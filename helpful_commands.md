# Helpful Commands

#### List the running unicorns and kill them
ps ax|grep gunicorn
pkill gunicorn

#### Create cloud function zip
zip -g function.zip main.py create_response.py lambda_config.py database_calls.py defaults.json requirements.txt

#### Build docker image for the model and run it
docker build -t deepcite_model .
PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} deepcite_model:latest

### Requires access to Google Cloud Platform

#### Connect to cloud sql
gcloud sql connect deepcite --user=postgres


#### Grab the password for accessing the database
gcloud secrets versions access 1 --secret="deepcite_db"