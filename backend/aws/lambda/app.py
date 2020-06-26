import json
import requests
import psycopg2
import sys
import base64
from dataclasses import dataclass
import time
import boto3
from botocore.exceptions import ClientError

# TODO: These should be env variables or imported from something better
versions = {'model': '0.2', 'lambda': '0.1', 'api': '0.1', 'extension': '0.1'}

secret_name = "rds_deepcite_sample"
region_name = "us-east-2"
db_name = 'postgres'

# Create a Secrets Manager client
session = boto3.session.Session()
secret_client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)

# private ip address of ec2
url = 'http://172.31.35.42:8000/api/v1/deep_cite'


def get_secret():
    print('grabbing secret')
    try:
        get_secret_value_response = secret_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print('error retrieving secret')
        print(e)
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return secret
    

# need this so that I can pass json or a response object to be returned
@dataclass
class Response:
    body: str
    status_code: int = 200

print('Loading function')

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
    
    print(event)
    stage = event['requestContext']['stage']

    if operation in operations:
        try:
            payload = load_payload(event)
            response = respond(None, operations[operation](payload))
        except Exception as e:
            print(e)
    else:
        response = respond(ValueError('Unsupported method "{}"'.format(operation)))

    user_id = event['requestContext']['http']['sourceIp']
    time_elapsed = time.time()-start
    secret = get_secret()

    try:
        secret = json.loads(secret)
        conn = psycopg2.connect(host=secret['host'], user=secret['username'], password=secret['password'], database=secret['dbInstanceIdentifier'], port=secret['port'])

        cur = conn.cursor()
        cur.execute("INSERT INTO deepcite_call (user_id,stage,status_code,response,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s)", (user_id,stage,response['statusCode'],response['body'],time_elapsed,json.dumps(versions)))
        conn.commit()
    except psycopg2.OperationalError as e:
        print("ERROR: Unexpected error: Could not connect to database instance.")
        print(e)
    else:
        print("SUCCESS: Connection to RDS instance succeeded")

    print(response)
        
    return response

# print(lambda_handler({"requestContext": {"http": {"method": "GET"}}},0))
