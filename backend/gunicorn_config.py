from config import config

bind = config['guincorn']['bind']
workers = config['guincorn']['workers'] 
timeout = config['guincorn']['timeout']