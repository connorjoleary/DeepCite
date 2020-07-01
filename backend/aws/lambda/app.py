import json
import requests
import psycopg2
import sys
import base64
from dataclasses import dataclass
import time
from lambda_config import config
import boto3
from botocore.exceptions import ClientError

# 1. allow for option where uuid is provided, then just retrieve response from database
# 2. split responce into extension or website, then if extension trim response to just being the few best sources
# 3. why does the deepcite extension in prod not look better

versions = {a: str(b) for a,b in config['versions'].items()}

# Create a Secrets Manager client
session = boto3.session.Session()
secret_client = session.client(
    service_name='secretsmanager',
    region_name=config['secret']['region']
)
new_submission = True

def get_secret():
    print('grabbing secret')
    try:
        get_secret_value_response = secret_client.get_secret_value(
            SecretId=config['secret']['name']
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
    # private ip address of ec2
    response = requests.post(url=config['ec2']['url'], json={"claim": claim, "link": link})
    new_submission = True
    return Response(body = response.text)

def grab_response(id, claim, link, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT response FROM deepcite_call where id = %s", (id)) #potentially this could just be a search by source claim and link and run for everything
        responses = conn.fetchall()
    except psycopg2.OperationalError as e:
        print("ERROR: Unexpected error: Could commit to database instance.")
        print(e)
        responses = []

    if len(responses) != 1:
        print('There were {} responses returned for the uuid {}'.format(len(responses), id))
        return call_deepcite(claim, link)
    else:
        new_submission=False
        return Response(body = responses[0])

def load_payload(event):
    if 'body' in event:
        body = event.get('body')
        return json.loads(base64.b64decode(body)) if event['isBase64Encoded'] else json.loads(body)
    return 'no body'

def lambda_handler(event, context):
    start = time.time()
    secret = get_secret()
    try:
        secret = json.loads(secret)
        conn = psycopg2.connect(host=secret['host'], user=secret['username'], password=secret['password'], database=secret['dbInstanceIdentifier'], port=secret['port'])
    except psycopg2.OperationalError as e:
        print("ERROR: Unexpected error: Could not connect to database instance.")
        print(e)
    else:
        print("SUCCESS: Connection to RDS instance succeeded")

    operations = {
        'POST': lambda x, conn: grab_response(x['id'], conn) if 'id' in x else call_deepcite(**x),
        'GET': lambda x, conn: Response(body= x, status_code= 200)
    }
    operation = event['requestContext']['http']['method']
    
    print(event)
    stage = event['requestContext']['stage']

    if operation in operations:
        try:
            payload = load_payload(event)
            response = respond(None, operations[operation](payload, conn))
        except Exception as e:
            print(e)
    else:
        response = respond(ValueError('Unsupported method "{}"'.format(operation)))

    user_id = event['requestContext']['http']['sourceIp']
    time_elapsed = time.time()-start

    try:
        cur = conn.cursor()
        if new_submission:
            cur.execute("INSERT INTO deepcite_retrieval (id,user_id,stage,status_code,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s)", (base_id, id, user_id,stage,response['statusCode'],time_elapsed,json.dumps(versions)))
        else:
            cur.execute("INSERT INTO deepcite_call (id,user_id,stage,status_code,response,response_time_elapsed,current_versions) VALUES (%s, %s, %s, %s, %s, %s, %s)", (base_id, id, user_id,stage,response['statusCode'],response['body'],time_elapsed,json.dumps(versions)))
        conn.commit()
    except psycopg2.OperationalError as e:
        print("ERROR: Unexpected error: Could commit to database instance.")
        print(e)
    
    print(response)
        
    return response

print(lambda_handler({"requestContext": {"http": {"method": "GET"}}},0))
