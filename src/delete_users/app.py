import boto3
import os
import json


def lambda_handler(message, context):

    if ('pathParameters' not in message or
            message['httpMethod'] != 'DELETE'):
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

    table = users_table.Table(table_name)
    user_id = message['pathParameters']['id']
    user_name = message['pathParameters']['username']
    

    params = {
        'id': user_id,
        'username': user_name
    }

    response = table.delete_item(
        Key=params
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'User deleted'})
    }