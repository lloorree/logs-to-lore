import argparse
import json
import logging
from os import listdir
from os.path import join

from model.converter import chatlogs_to_lorebook
from model.encoder import EnhancedJSONEncoder
from model.silly_tavern import SillyBook
from model.tavern import TavernEntry

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG, force=True)
    logging.info('Converting chatlogs to lorebook.')
    parser = argparse.ArgumentParser(description='Run defined model on supplied data.')
    parser.add_argument('-output_name', dest="output_name", type=str, help='Name of the output book.',
                        default='Logs2Lore')
    parser.add_argument('-source_folder', dest="source_folder", type=str,
                        help='Absolute or relative path of folder with chatlog files.',
                        default='test_inputs')
    parser.add_argument('-target_file', dest="target_file", type=str,
                        help='Absolute or relative path of desired target file.',
                        default='test_outputs/output_silly_book.json')
    parser.add_argument('-user_name', dest="user_name", type=str,
                        help='The name to replace any undifferentiated \'You\' speaker with.',
                        default='USER')
    parser.add_argument('-max_keywords', dest="max_keywords", type=int,
                        help='Max keywords per entry.',
                        default=10)
    args: argparse.Namespace = parser.parse_args()
    logging.info('Using args: %s', args)
    messages = []
    excluded_keywords = set()
    for filename in listdir(args.source_folder):
        with open(join(args.source_folder, filename), 'r') as source_file:
            lines = source_file.readlines()[1:]
            entries: [TavernEntry] = [TavernEntry(**json.loads(line), user_override=args.user_name) for line in lines]
            sub_messages = []
            for entry in entries:
                excluded_keywords.add(entry.name)
                excluded_keywords = excluded_keywords.union(set(entry.name.split(' ')))
                sub_messages.append(entry.name + ': ' + entry.mes)
            messages.append(sub_messages)
    book: SillyBook = chatlogs_to_lorebook(messages, args.output_name, excluded_keywords, args.max_keywords)
    with open(args.target_file, 'w') as outfile:
        json.dump(book, outfile, cls=EnhancedJSONEncoder, indent=4)
    logging.info('Done.')
