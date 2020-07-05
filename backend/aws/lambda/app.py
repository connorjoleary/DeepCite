import json
import requests
import psycopg2
import sys
import base64
from dataclasses import dataclass
import time
from lambda_config import config
import traceback
from create_response import respond
import boto3
from botocore.exceptions import ClientError
import uuid

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

print('Loading function')

def call_deepcite(claim, link, **kwargs):
    # private ip address of ec2
    response = requests.post(url=config['ec2']['url'], json={"claim": claim, "link": link})
    new_submission = True
    return json.loads(response.text)

def grab_response(conn, id, claim, link, **kwargs):
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
        return responses[0] #not sure if i need json loads

def load_payload(event):
    if 'body' in event:
        body = event.get('body')
        return json.loads(base64.b64decode(body)) if event['isBase64Encoded'] else json.loads(body)
    raise('No body in payload')

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
        'POST': lambda x, conn: grab_response(conn, **x) if 'id' in x else call_deepcite(**x)
    }
    operation = event['requestContext']['http']['method']
    
    print(event)
    stage = event['requestContext']['stage']

    if operation in operations:
        try:
            payload = load_payload(event)
            response = operations[operation](payload, conn)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            response = e
    else:
        response = Exception(f'Unsupported method "{operation}"')
        payload = {}
    
    print(response)

    user_id = event['requestContext']['http']['sourceIp']
    if isinstance(response, Exception):
        base_id = str(uuid.uuid4())
    else:
        base_id = response['results'][0]['citeID']

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

    return respond(payload.get('response_size', 'small'), response)

# body = "{\"id\": \"fdaeasfsd\", \"resonse_size\": \"small\", \"claim\":\"the death of Sherlock Holmes almost destroyed the magazine thries. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.\", \"link\":\"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world\"}"
# print(lambda_handler({"isBase64Encoded": False, "body": body, "requestContext": {"http": {"method": "POST", "sourceIp": "dfsds"}, "stage": "dev", }},0))
