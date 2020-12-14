import boto3
import os
import json


def lambda_handler(event, context):

    if ('httpMethod' not in event or
            event['httpMethod'] != 'GET'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'Users')
    region = os.environ.get('REGION', 'ap-southeast-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    client = boto3.client('dynamodb')
    StartKey = None
    
    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
    TableName='Users', Select='ALL_ATTRIBUTES',
    ConsistentRead=True,
    # FilterExpression='UserName',
    PaginationConfig={
        'MaxItems': 10,
        'PageSize': 10,
        'StartingToken': 'StartKey'
    }
)

   # extract the results
    items = response_iterator['Items']
    for item in items:
        print(item)

    queryCount += 1

    while 'LastEvaluatedKey' in response_iterator:    
        StartKey = response_iterator['LastEvaluatedKey']
        items = response['Items']
        for item in items:
            print(item)
        

    return {
     'statusCode': 200,
     'headers': {},
     'body': json.dumps()