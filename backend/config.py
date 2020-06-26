import os
import json
from os import environ as env
from pprint import pprint
from configparser import ConfigParser
from cerberus import Validator

config_validator = Validator({
	'file_path' : {
		'type': 'string',
		'required': True,
	},
	'cwd' : {
		'type': 'string',
		'required': True,
	},
	'env': {
		'type': 'string',
		'required': True,
	},
	'gunicorn': {
		'type': 'dict',
		'required': True,
		'schema': {
			'bind': { 'type': 'string' },
			'host': { 'type': 'string' },
			'port': { 'type': 'integer' },
			'workers': { 'type': 'integer' },
			'timeout': { 'type': 'integer' },
		},
	},
	'server': {
		'type': 'dict',
		'required': True,
		'schema': {
			'host': { 'type': 'string' },
			'port': { 'type': 'integer' },
		},
	},
	'gn_path': {
		'type': 'string',
		'required': True,
	},
	'language': {
		'type': 'string',
		'required': True,
	},
})

CONFIG_FILENAME = 'deep-cite-config.json'
CWD = os.getcwd()

config_file = env.get('CONFIG_FILE') or os.path.join(CWD, '..', CONFIG_FILENAME)

if os.path.exists(config_file):
	try:
		with open(config_file) as f:
			config_json = json.load(f)
	except json.JSONDecodeError:
		config = {}
	else:
		config = config_json['backend']
else:
	config = {}

config['file_path'] = config_file
config['cwd'] = CWD

DEFAULT = {
	'ENV': 'development',
	'LANGUAGE': 'en',
	'GN_PATH': os.path.join(CWD, 'word_vectors', 'GoogleNews-vectors-negative300.bin'),
	'SERVER': {
		'HOST': '0.0.0.0',
		'PORT': 5000,
	},
	'GUNICORN': {
		'HOST': '0.0.0.0',
		'PORT': 8000,
		'WORKERS': 1,
		'TIMEOUT': 3 * 60,
	},
}

config['env'] = config.get('env') or env.get('ENV') or DEFAULT['ENV']
config['language'] = config.get('language') or env.get('LANGUAGE') or DEFAULT['LANGUAGE']
config['gn_path'] = config.get('gn_path') or env.get('GN_PATH') or DEFAULT['GN_PATH']

server = config.get('server', {})
server['host'] = server.get('host') or env.get('SERVER_HOST') or DEFAULT['SERVER']['HOST']
server['port'] = server.get('port') or env.get('SERVER_PORT') or DEFAULT['SERVER']['PORT']
config['server'] = server

gunicorn = config.get('gunicorn', {})
gunicorn['host'] = gunicorn.get('host') or env.get('GUNICORN_HOST') or DEFAULT['GUNICORN']['HOST']
gunicorn['port'] = gunicorn.get('port') or env.get('GUNICORN_PORT') or DEFAULT['GUNICORN']['PORT']
gunicorn['bind'] = gunicorn.get('bind') or env.get('GUNICORN_BIND') or f"{gunicorn['host']}:{gunicorn['port']}"
gunicorn['workers'] = gunicorn.get('workers') or env.get('GUNICORN_WORKERS') or DEFAULT['GUNICORN']['WORKERS']
gunicorn['timeout'] = gunicorn.get('timeout') or env.get('GUNICORN_TIMEOUT') or DEFAULT['GUNICORN']['TIMEOUT']
config['gunicorn'] = gunicorn


config_validator.validate(config)
if config_validator.errors:
	print("Invalid Config:")
	pprint(json.dumps(config_validator.errors, indent=4))
	exit(1)

config = config_validator.document