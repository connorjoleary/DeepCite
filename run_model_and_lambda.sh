pkill gunicorn

cd backend/model
source v-env-test/bin/activate
gunicorn -c gunicorn_config.py wsgi --daemon

cd ../../backend/lambda
source v-env-test/bin/activate
gunicorn -c gunicorn_config.py wsgi:app --daemon
