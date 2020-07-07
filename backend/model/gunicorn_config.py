from config import config as file_config

bind = file_config['gunicorn']['bind']
workers = file_config['gunicorn']['workers'] 
timeout = file_config['gunicorn']['timeout']