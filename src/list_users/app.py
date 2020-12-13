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
    
    paginator = client.get_paginator('scan')
    pages = paginator.paginate(
    TableName='Users', Select='ALL_ATTRIBUTES',
    ConsistentRead=True,
    PaginationConfig={
        'MaxItems': 10,
        'PageSize': 10,
    }
)
    for page in pages:
	    print(page)
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(page)
    }
