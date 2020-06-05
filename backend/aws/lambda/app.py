import json
import requests
import psycopg2
import sys

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

def respond(err, res=None):

    return {
        'statusCode': '400' if err else res.status_code,
        'body': err.message if err else res.json(),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def call_deepcite(claim, link):
    return requests.post(url=url, json={"claim": claim, "link": link})
    

def lambda_handler(event, context):

    operations = {
        'POST': lambda x: call_deepcite(**x)
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation](payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))

# print(lambda_handler({"body": "{\"claim\": \"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event\",\"link\": \"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world\"}","httpMethod": "POST"},0))
