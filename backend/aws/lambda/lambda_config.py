import os
import json
from os import environ as env

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
    'SECRET': {
        'REGION': "us-east-2",
        'NAME': "rds_deepcite_sample",
    },
    'VERSIONS': {
        'MODEL': 0.3,
        'LAMBDA': 0.2,
        'API': 0.2,
        'EXTENSION': 0.2,
    },
    'RESPONSE': {
        'NUM_BEST_RETURNED': 3
    }
}

config['env'] = config.get('env') or env.get('ENV') or DEFAULT['ENV']

ec2 = config.get('ec2', {})
ec2['ip'] = ec2.get('ip') or env.get('EC2_IP') or DEFAULT['EC2']['IP']
ec2['port'] = ec2.get('port') or env.get('EC2_PORT') or DEFAULT['EC2']['PORT']
ec2['url'] = ec2.get('url') or env.get('EC2_URL') or f"http://{ec2['ip']}:{ec2['port']}/api/v1/deep_cite"
config['ec2'] = ec2

secret = config.get('secret', {})
secret['region'] = secret.get('region') or env.get('SECRET_REGION') or DEFAULT['SECRET']['REGION']
secret['name'] = secret.get('name') or env.get('SECRET_NAME') or DEFAULT['SECRET']['NAME']
config['secret'] = secret

versions = config.get('versions', {})
versions['model'] = versions.get('model') or env.get('VERSIONS_MODEL') or DEFAULT['VERSIONS']['MODEL']
versions['lambda'] = versions.get('lambda') or env.get('VERSIONS_LAMBDA') or DEFAULT['VERSIONS']['LAMBDA']
versions['api'] = versions.get('api') or env.get('VERSIONS_API') or DEFAULT['VERSIONS']['API']
versions['extension'] = versions.get('extension') or env.get('VERSIONS_EXTENSION') or DEFAULT['VERSIONS']['EXTENSION']
config['versions'] = versions

response = config.get('response', {})
response['num_best_returned'] = response.get('num_best_returned') or env.get('RESPONSE_NUM_BEST_RETURNED') or DEFAULT['RESPONSE']['NUM_BEST_RETURNED']
config['response'] = response