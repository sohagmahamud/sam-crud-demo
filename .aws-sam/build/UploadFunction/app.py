import boto3
import os
import json
import uuid
from datetime import datetime
import base64
import csv
import logging
from botocore.exceptions import ClientError


def s3create():
    
    # Create bucket
    region = 'ap-southeast-1'
    bucket_name = 'sam-crud-csv-bucket'
    
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
def lambda_handler(event, context):    
    
    # write csv to s3 from api gateway /upload endpoint.
    
    if ('body' not in event or
            event['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
        
    file_content = base64.b64decode(event['content'])
    file_path = 'sample.csv'
    s3 = boto3.client('s3')
    try:
        s3_response = s3.put_object(Bucket=bucket_name, Key=file_path, Body=file_content)
    except Exception as e:
        raise IOError(e)
    return {
        'statusCode': 200,
        'body': {
            'file_path': file_path
        }
    }    
    
def dynamowrite():    
    
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


    file_content = base64.b64decode(event['content'])
    
    try:

        record_list = (x.strip() for x in file_content['Body'].read().decode('utf-8').split('\r\n'))
        csv_reader = csv.reader(record_list, delimiter=',', quotechar='"')
        headers = next(csv_reader)
        now = datetime.now()
        x = now.strftime("%m/%d/%Y, %H:%M:%S")
        
        for row in csv_reader:
            UserName = row[0]
            add_to_db = users_table.put_item(
                TableName = "Users",
                Item = {
                    'username' : {'S' : str(UserName)},
                    'date' : {'S' : x}
                })
    
    except Exception as e:
        print(str(e))
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success! Users in CSV uploaded to DynamoDB.')
    }