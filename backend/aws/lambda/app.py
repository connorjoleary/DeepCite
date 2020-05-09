import boto3

def handler(event, context):
    client = boto3.client('ecs')

    claim = event['claim']
    link = event['link']

    return {'status': 200, 'message': "still in progress"}