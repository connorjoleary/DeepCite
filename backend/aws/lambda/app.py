import boto3

def handler(event, context):
    client = boto3.client('runtime.sagemaker')
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=payload)

    print(client.list_clusters())
    print()
    response = client.run_task(**params)
    print(response)
    return {'status': 200, 'response': "in progress"}