import boto3
import os
import json


def lambda_handler(event, context):

    if ('pathParameters' not in event or
            event['httpMethod'] != 'DELETE'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    region = os.environ.get('REGION', 'ap-southeast-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    if aws_environment == 'AWS_SAM_LOCAL':
        users_table = boto3.client(
            'dynamodb',
            endpoint_url='http://dynamodb:8000'
        )
    else:
        users_table = boto3.client(
            'dynamodb',
            region_name=region
        )
    users_table = boto3.client('dynamodb')
    data = event['pathParameters']
    params = {
        'id': {'S' : data['id']}
        # 'username' : {'S' : data['username']} Not passing this value since our table only has primary partition key defined.
    }

    response = users_table.delete_item(
        TableName = "Users",
        Key=params
       )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'User deleted'})
    }