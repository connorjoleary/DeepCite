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
import uuid
from unittest import mock
# from database_calls import database_calls

versions = {a: str(b) for a,b in config['versions'].items()}

new_submission = True

print('Loading function')

def call_deepcite(claim, link, **kwargs):
    # private ip address of ec2
    response = requests.post(url=config['ec2']['url'], json={"claim": claim, "link": link})
    new_submission = True
    return json.loads(response.text)

def grab_response(database_calls, id, claim, link, **kwargs):
    responses = database_calls.grab_deepcite_entry(id)

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

    if event.get('test', False):
        database_calls = mock.Mock()
        database_calls.grab_deepcite_entry = lambda id: []
        database_calls.record_call = lambda *x: None
    else:
        from database_calls import database_calls
        database_calls = database_calls()


    operations = {
        'POST': lambda x, database_calls: grab_response(database_calls, **x) if 'id' in x else call_deepcite(**x)
    }
    operation = event['requestContext']['http']['method']
    
    print(event)
    stage = event['requestContext']['stage']

    if operation in operations:
        try:
            payload = load_payload(event)
            response = operations[operation](payload, database_calls)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            response = e
    else:
        response = Exception('Unsupported method "{}"'.format(operation))
        payload = {}

    user_id = event['requestContext']['http']['sourceIp']
    if isinstance(response, Exception):
        base_id = str(uuid.uuid4())
    else:
        base_id = response['results'][0]['citeID']

    time_elapsed = time.time()-start
    database_calls.record_call(base_id, id, user_id, stage, response, time_elapsed, versions)

    response = respond(payload.get('response_size', 'small'), response)
    print(response)
    return response

# body = "{\"id\": \"fdaeasfsd\", \"resonse_size\": \"small\", \"claim\":\"the death of Sherlock Holmes almost destroyed the magazine thries. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.\", \"link\":\"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world\"}"
# print(lambda_handler({"isBase64Encoded": False, "body": body, "requestContext": {"http": {"method": "POST", "sourceIp": "dfsds"}, "stage": "dev", }},0))
