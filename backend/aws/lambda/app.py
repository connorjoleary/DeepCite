import json
import requests

print('Loading function')
# -H "Content-Type: application/json"
url = 'http://3.19.211.248:5000/api/v1/deep_cite'


def respond(err, res=None):
    print(res)
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,#json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def call_deepcite(claim, link):
    return requests.post(url=url, params={"claim": claim, "link": link}).json()
    

def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'POST': lambda x: call_deepcite(**x)
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation](payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))

# curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”."
# , "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' 
# -H "Content-Type: application/json" 
# -X POST http://3.19.211.248:5000/api/v1/deep_cite