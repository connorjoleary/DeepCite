# Helpful Commands

#### List the running unicorns and kill them
ps ax|grep gunicorn
pkill gunicorn

#### Create cloud function zip
zip -g function.zip main.py create_response.py lambda_config.py database_calls.py defaults.json requirements.txt

#### Build docker image for the model and run it
docker build -t deepcite_model .
PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} deepcite_model:latest

### Python Profiling

#### Create memory profile of model
mprof run --include-children python main.py
mprof plot --output mem-plot.png

#### Create time profile of model
python -m cProfile -o profile main.py
python profile_stats.py

### Requires access to Google Cloud Platform

#### Connect to cloud sql
gcloud sql connect deepcite --user=postgres


#### Grab the password for accessing the database
gcloud secrets versions access 1 --secret="deepcite_db"

