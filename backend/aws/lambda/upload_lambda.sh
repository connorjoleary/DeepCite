cd v-env/lib/python3.6/site-packages
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip app.py controller.py exceptions.py tree.py wiki_scraper.py
aws lambda update-function-code --function-name deepcite --zip-file fileb://function.zip