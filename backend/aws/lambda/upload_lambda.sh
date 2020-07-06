cd v-env/lib/python3.7/site-packages
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip app.py create_response.py lambda_config.py
aws lambda update-function-code --function-name deepcite --zip-file fileb://function.zip