import boto3

def handler(event, context):
    client = boto3.client('ecs')

    claim = event['claim']
    link = event['link']

    params = {'taskDefinition': 'deepcite',
            'cluster': 'arn:aws:ecs:us-east-2:072491736148:cluster/deepcite',
            'launchType': 'FARGATE',
            'networkConfiguration':
                {'awsvpcConfiguration': 
                    {'subnets': [
                        'subnet-05452e5640c015db2',
                    ],
                    'securityGroups': [
                        'sg-0d1b015575624679e',
                    ],
                    'assignPublicIp': 'DISABLED'}
            },
            'overrides':
                {'containerOverrides': [
                    {'name': 'deepcite', 'environment': [
                            {'name': 'claim', 'value': claim
                            },
                            {'name': 'link', 'value': link
                            }
                        ]
                    }
                ]
            }
        }

    print(client.list_clusters())
    print()
    response = client.run_task(**params)
    print(response)
    return {'status': 200, 'response': "in progress"}