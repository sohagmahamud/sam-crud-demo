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

    results = []
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = client.scan(
                TableName=table_name,
                ExclusiveStartKey=last_evaluated_key
            )
        else: 
            response = client.scan(TableName=table_name)
            last_evaluated_key = response.get('LastEvaluatedKey')
            results.extend(response['Items'])
        
        if not last_evaluated_key:
            break
            
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(results)
    }