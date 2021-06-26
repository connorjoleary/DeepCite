import json
import requests
import sys
import base64
import time
from lambda_config import config
import traceback
from create_response import respond
import uuid
from unittest import mock

versions = {a: str(b) for a,b in config['versions'].items()}

print('Loading function')

# TODO: why are the stored events scored with 1 (ex id:b39a196c-da57-46b6-8d4d-03ff88b62fbb)

def call_deepcite(claim, link, **kwargs):
    # private ip address of ec2
    response = requests.post(url=config['CLOUDRUN']['url']+'/api/v1/deep_cite', json={"claim": claim, "link": link})
    print(response)
    return json.loads(response.text)

def grab_response(database_calls, claim, link, **kwargs):
    responses = database_calls.grab_deepcite_entry(id) if 'id' in kwargs else database_calls.check_repeat(claim, link, versions)

    print('There were {} responses returned'.format(len(responses)))
    if len(responses) == 0:
        return (call_deepcite(claim, link), None)
    else:
        existing_id = responses[0][0]
        existing_response = responses[0][1]
        return (existing_response, existing_id) #not sure if I need json loads

def record_call(response, start, database_calls, user_id, stage, existing_id):

    print('Deepcite response:', response)

    if isinstance(response, Exception):
        base_id = str(uuid.uuid4())
    else:
        base_id = response['results'][0]['citeID']

    time_elapsed = time.time()-start

    lambda_response = respond(response)
    try:
        database_calls.record_call(existing_id, base_id, user_id, stage, 200, response, time_elapsed, versions) # TODO:figure out status code
    except Exception as e:
        print("unable to store call")
        traceback.print_tb(e.__traceback__)
        print(e)
    return lambda_response

def lambda_handler(event):
    event = event.get_json(silent=True)
    start = time.time()

    if event.get('test', False):
        database_calls = mock.Mock()
        database_calls.grab_deepcite_entry = lambda id: []
        database_calls.record_call = lambda *x: None
        database_calls.record_source = lambda *x: None
    else:
        from database_calls import DatabaseCalls
        database_calls = DatabaseCalls()
    
    print(event)
    stage = event['stage']
    user_id = event['ip']

    if event.get('type') == "source":
        source_id = event.get('sourceId')
        base_id = event.get('baseId')
        
        results = f"The source: {source_id} for base id: {base_id} has been noted"
        error = None
        try:
            database_calls.record_source(base_id, source_id, user_id, stage, versions)
        except Exception as e:
            print("Unable to store source")
            traceback.print_tb(e.__traceback__)
            print(e)
            error = e
            results = None

        return {'error': error, 'results': results}

    response, existing_id = grab_response(database_calls, **event)

    return record_call(response, start, database_calls, user_id, stage, existing_id)

# body = "{\"ip\": \"127.0.0.1\", \"test\": false, \"stage\": \"dev\", \"resonse_size\": \"small\", \"claim\":\"That the first novel featuring time travel was written in 1733. It is set 1997 and tells of a future where the world becomes dominated by the Jesuits. Because it was written before the industrial revolution, there is no depicted technological advancement between the authors time and the future\", \"link\":\"https://www.reddit.com/r/todayilearned/comments/nz68d1/til_that_the_first_novel_featuring_time_travel\"}"
# body = "{\"ip\": \"127.0.0.1\", \"test\": true, \"stage\": \"dev\", \"id\": \""+str(uuid.uuid4())+"\", \"resonse_size\": \"small\", \"claim\":\"the death of Sherlock Holmes almost destroyed the magazine thries. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.\", \"link\":\"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world\"}"

# print(lambda_handler(json.loads(body)))#{"isBase64Encoded": False, "body": body, "requestContext": {"http": {"method": "POST", "sourceIp": "dfsds"}, "stage": "dev", }},0))
