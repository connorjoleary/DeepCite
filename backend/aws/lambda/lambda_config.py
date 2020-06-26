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
    'versions': {
        'type': 'dict',
        'required': True,
        'schema': {
            'model': { 'type': 'float', 'coerce': float, },
            'lambda': { 'type': 'float', 'coerce': float, },
            'api': { 'type': 'float', 'coerce': float, },
            'extension': { 'type': 'float', 'coerce': float, },
        },
    },
    'db': {
        'type': 'dict',
        'required': True,
        'schema': {
            'name': { 'type': 'string' },
            'password': { 'type': 'string' },
            'username': { 'type': 'string' },
            'rds': { 'type': 'string' },
            'port': { 'type': 'integer', 'coerce': int, },
        },
    },
    'ec2': {
        'type': 'dict',
        'required': True,
        'schema': {
            'ip': { 'type': 'string' },
            'port': { 'type': 'integer', 'coerce': int, },
            'url': { 'type': 'string' },
        },
    },
})

CONFIG_FILENAME = 'deep-cite-config.json'
CWD = os.getcwd()

config_file = env.get('CONFIG_FILE') or os.path.join(CWD, '..', '..', '..', CONFIG_FILENAME)

if os.path.exists(config_file):
    try:
        with open(config_file) as f:
            config_json = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing json config file: {e}")
        config = {}
    else:
        config = config_json['aws']
else:
    config = {}

config['file_path'] = config_file
config['cwd'] = CWD

DEFAULT = {
    'ENV': 'development',
    'EC2': {
        'IP': '172.31.35.42',
        'PORT': 8000,
    },
    'DB': {
        'RDS': "deepcite.ckbyp3nhsmiu.us-east-2.rds.amazonaws.com",
        'NAME': 'postgres',
        'PORT': 5432,
        'USERNAME': 'postgres',
        'PASSWORD': 'deepcite',
    },
    'VERSIONS': {
        'MODEL': 0.1,
        'LAMBDA': 0.1,
        'API': 0.1,
        'EXTENSION': 0.1,

    },
}

config['env'] = config.get('env') or env.get('ENV') or DEFAULT['ENV']

ec2 = config.get('ec2', {})
ec2['ip'] = ec2.get('ip') or env.get('EC2_IP') or DEFAULT['EC2']['IP']
ec2['port'] = ec2.get('port') or env.get('EC2_PORT') or DEFAULT['EC2']['PORT']
ec2['url'] = ec2.get('url') or env.get('EC2_URL') or f"http://{ec2['ip']}:{ec2['port']}/api/v1/deep_cite"
config['ec2'] = ec2

db = config.get('db', {})
db['rds'] = db.get('rds') or env.get('DB_RDS') or DEFAULT['DB']['RDS']
db['port'] = db.get('port') or env.get('DB_PORT') or DEFAULT['DB']['PORT']
db['name'] = db.get('name') or env.get('DB_NAME') or DEFAULT['DB']['NAME']
db['username'] = db.get('username') or env.get('DB_USERNAME') or DEFAULT['DB']['USERNAME']
db['password'] = db.get('password') or env.get('DB_PASSWORD') or DEFAULT['DB']['PASSWORD']
config['db'] = db

versions = config.get('versions', {})
versions['model'] = versions.get('model') or env.get('VERSIONS_MODEL') or DEFAULT['VERSIONS']['MODEL']
versions['lambda'] = versions.get('lambda') or env.get('VERSIONS_LAMBDA') or DEFAULT['VERSIONS']['LAMBDA']
versions['api'] = versions.get('api') or env.get('VERSIONS_API') or DEFAULT['VERSIONS']['API']
versions['extension'] = versions.get('extension') or env.get('VERSIONS_EXTENSION') or DEFAULT['VERSIONS']['EXTENSION']
config['versions'] = versions

config_validator.validate(config)
if config_validator.errors:
    print("Invalid Config:")
    pprint(json.dumps(config_validator.errors, indent=4))
    exit(1)

config = config_validator.document