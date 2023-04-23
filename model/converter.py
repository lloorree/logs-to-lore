from typing import Dict

import yake
from transformers import pipeline

from model.silly_tavern import SillyBook, SillyEntry


def chatlogs_to_lorebook(messages: [[str]], name: str, excluded_keywords=None, max_keywords=10) -> SillyBook:
    if excluded_keywords is None:
        excluded_keywords = set()
    summaries: Dict[str, SillyEntry] = {}
    if len(messages) == 0:
        return SillyBook(name, '', summaries)

    # single extractor and summarizer instance per conversion since I don't know if it is thread-safe.
    kw_extractor = yake.KeywordExtractor()
    summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")
    # faster but sucks: "sshleifer/distilbart-cnn-12-6"         (1.366 s  on tower example)
    # faster but sucks: "facebook/bart-large-cnn"               (2.590 s  on tower example)
    # slow and sucks: "google/pegasus-cnn_dailymail"            (4.487 s  on tower example)
    # WINNER: "philschmid/bart-large-cnn-samsum"                (14.368 s on tower example, but not that slow here?)
    uid = 1
    for chat_log in messages:
        current_text = ''
        current_keywords = set()
        priority_weight = 0
        index = 0
        length_limit = len(chat_log)
        while index < length_limit:
            message = chat_log[index]
            index += 1
            msg_keywords = kw_extractor.extract_keywords(message)
            uniq = {kw[0] for kw in msg_keywords if kw[0] not in excluded_keywords}
            has_key = False
            if len(current_keywords) <= 4 or priority_weight <= 4:
                current_keywords = current_keywords.union(uniq)
                priority_weight += 1
                has_key = True
            else:
                for key in uniq:
                    if key in current_keywords:
                        has_key = True
                        priority_weight += 1
                        current_keywords = current_keywords.union(uniq)
                        break
            if not has_key or index == length_limit:
                summary = summarize(current_text, summarizer)
                keywords = kw_extractor.extract_keywords(current_text)
                # arbitrarily use the first X keywords.
                legitimate_keywords = [kw[0] for kw in keywords if kw[0] not in excluded_keywords]
                summaries[str(uid)] = SillyEntry(uid, legitimate_keywords[:max_keywords], [],
                                                 legitimate_keywords[0], summary,
                                                 constant=False, selective=False, order=priority_weight,
                                                 position=priority_weight)
                uid += 1
                current_text = message + '\n'
                current_keywords = uniq
                priority_weight = 0
            else:
                current_text += message + '\n'
    book: SillyBook = SillyBook(name, '', summaries)
    return book


def summarize(text: str, model, max_length: int = 500):
    combined_summary = None
    if len(text) > 4000:
        for separator in ['\n', '. ']:
            if separator in text:
                sents = text.split(separator) if combined_summary is None else combined_summary.split(separator)
                halfway = int(len(sents) / 2)
                first = summarize(separator.join(sents[:halfway]), model, max_length)
                second = summarize(separator.join(sents[halfway:]), model, max_length)
                combined_summary = first + separator + second
                if len(combined_summary) > max_length:
                    combined_summary = summarize(combined_summary, model, max_length)
                if len(combined_summary) <= max_length:
                    break
    else:
        combined_summary = model(text)[0]['summary_text']
    return combined_summary
