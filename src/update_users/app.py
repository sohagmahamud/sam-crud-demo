import boto3
import os
import json

def lambda_handler(event, context):
    
    if ('body' not in event or
            event['httpMethod'] != 'PUT'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    
    table_name = os.environ.get('TABLE', 'Users')
    region = os.environ.get('REGION', 'ap-southeast-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    if aws_environment == 'AWS_SAM_LOCAL':
        users_table = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb:8000'
        )
    else:
        users_table = boto3.resource(
            'dynamodb',
            region_name=region
        )
    print(event)
    data = json.loads(event['body'])
    table = users_table.Table(table_name)
    
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          ':s': 'username',
        },
        ExpressionAttributeValues={
          ':username': data['username']
        },
        UpdateExpression='SET username= :username, ',
        ReturnValues='UPDATED_NEW',
    )


    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(result['Attributes'])
    }
