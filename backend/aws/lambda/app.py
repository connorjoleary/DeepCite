import json
import requests
import psycopg2
import sys
import base64
from dataclasses import dataclass
import time
from lambda_config import config


# TODO: These should be env variables or imported from something better
versions = {'model': 0.1, 'lambda': 0.1, 'api': 0.1, 'extension': 0.1}

rds_host  = "deepcite.ckbyp3nhsmiu.us-east-2.rds.amazonaws.com"
db_name = 'postgres'
db_password = 'deepcite'
db_username = 'postgres'

print('Loading function')

# private ip address of ec2
url = 'http://172.31.35.42:8000/api/v1/deep_cite'

try:
    conn = psycopg2.connect(host=rds_host, user=db_username, password=db_password, database=db_name, port='5432')
except psycopg2.OperationalError as e:
    print("ERROR: Unexpected error: Could not connect to database instance.")
    print(e)
    sys.exit()
print("SUCCESS: Connection to RDS instance succeeded")

# need this so that I can pass json or a response object to be returned
@dataclass
class Response:
    body: str
    status_code: int = 200


def respond(err, res=None):
    return {
        'statusCode': '400' if err else res.status_code,
        'body': err.message if err else res.body
    }

def call_deepcite(claim, link):
    response = requests.post(url=url, json={"claim": claim, "link": link})
    return Response(body = response.text)

def load_payload(event):
    if 'body' in event:
        body = event.get('body')
        return json.loads(base64.b64decode(body)) if event['isBase64Encoded'] else json.loads(body)
    return 'no body'

def lambda_handler(event, context):
    start = time.time()

    operations = {
        'POST': lambda x: call_deepcite(**x),
        'GET': lambda x: Response(body= x, status_code= 200)
    }
    operation = event['requestContext']['http']['method']
    
    # print(event)
    stage = event['requestContext']['stage']

    if operation in operations:
        payload = load_payload(event)
        response = respond(None, operations[operation](payload))
    else:
        response = respond(ValueError('Unsupported method "{}"'.format(operation)))

    user_id = event['requestContext']['http']['sourceIp']
    time_elapsed = time.time()-start
    
    cur = conn.cursor()
    cur.execute("INSERT INTO deepcite_call (user_id,stage,status_code,response,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s)", (user_id,stage,response['statusCode'],response['body'],time_elapsed,json.dumps(versions)))
    conn.commit()

    return response

# print(lambda_handler({"requestContext": {"http": {"method": "GET"}}},0))
