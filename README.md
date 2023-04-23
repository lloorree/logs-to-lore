### Janky SillyTavern Chat Log to Lorebook Conversion

Results may vary from perfect to unusable garbage.

Use the pip_freeze_result.txt for venv setup if the requirements.txt is wrong.

Usage like:

```
python logs_to_lore.py -output_name Logs2Lore -source_folder test_inputs \ 
    -user_name Lore -target_file test_outputs/output_silly_book.json -max_keywords 10
```