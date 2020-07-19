source v-env/bin/activate
zip -g function.zip claim.py config.py exceptions.py main.py tokenizer.py tree.py wiki_scraper.py
aws lambda update-function-code --function-name deepcite_model --zip-file fileb://function.zip