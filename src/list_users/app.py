import boto3
import os
import json
from botocore.paginate import TokenEncoder

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

    if aws_environment == 'AWS_SAM_LOCAL':
        client = boto3.client(
            'dynamodb',
            endpoint_url='http://dynamodb:8000'
        )
    else:
        client = boto3.client(
            'dynamodb',
            region_name=region
        )

    pagination_config={
            "MaxItems":20, 
            "PageSize": 5
            }
    
    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        TableName=table_name, 
        PaginationConfig=pagination_config
    )
    for page in response_iterator:
        Items = page['Items']
        print(Items)
        print("--------------------------")

    
    encoder = TokenEncoder()
    for page in response_iterator:
        if "LastEvaluatedKey" in page:
            encoded_token = encoder.encode({"ExclusiveStartKey": page["LastEvaluatedKey"]})
            pagination_config = {
                    "MaxItems": 20,
                    "PageSize": 5,
                    "StartingToken": encoded_token
                    }
            Items = page['Items']
            
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(Items)
    }