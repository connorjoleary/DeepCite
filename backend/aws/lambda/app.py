import json
import requests
import sys
import base64
from dataclasses import dataclass
import time
import boto3
from botocore.exceptions import ClientError

# TODO: These should be env variables or imported from something better
versions = {'model': 0.1, 'lambda': 0.1, 'api': 0.1, 'extension': 0.1}
secret_name = "rds_deepcite_sample"
region_name = "us-east-2"
db_name = 'postgres'

# Create a Secrets Manager client
session = boto3.session.Session()
secret_client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)
rds_client = session.client(
    service_name='rds-data',
    region_name=region_name
)

print('Loading function')

# private ip address of ec2
url = 'http://172.31.35.42:8000/api/v1/deep_cite'


def get_secret():
    print('grabbing secret')
    try:
        get_secret_value_response = secret_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            print(e)
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            print(e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            print(e)
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            print(e)
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            print(e)
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    print(secret)
    return secret
    

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
    print('got here')
    print("INSERT INTO deepcite_call (user_id,stage,status_code,response,response_time_elapsed,current_versions) VALUES ('{}', '{}', {}, '{}', {}, '{}')".format(user_id,stage,response['statusCode'],response['body'].replace("'", ""),time_elapsed,json.dumps(versions)))
    try:
        rds_response = rds_client.execute_statement(
            resourceArn ='arn:aws:rds:us-east-2:072491736148:db:deepcite',
            # database=db_name,
            secretArn='arn:aws:secretsmanager:us-east-2:072491736148:secret:rds_deepcite_sample-Y9B0Sa',
            sql ="INSERT INTO deepcite_call (user_id,stage,status_code,response,response_time_elapsed,current_versions) VALUES ('{}', '{}', {}, '{}', {}, '{}')".format(user_id,stage,response['statusCode'],response['body'].replace("'", ""),time_elapsed,json.dumps(versions))
        )
        print(rds_response)
    except Exception as e:
        print(e)
    print(response)
        
    return response

# print(lambda_handler({"requestContext": {"http": {"method": "GET"}}},0))
