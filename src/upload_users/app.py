import boto3
import os
import json
from datetime import datetime
import base64
import csv
import uuid
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = 'ap-southeast-1'
bucket_name = 'sam-crud-csv-bucket'

def lambda_handler(event, context):
    
    file_content = base64.b64decode(event['body'])
    file_path = 'sample.csv'
    s3 = boto3.client('s3')
    s3_response = s3.put_object(Bucket=bucket_name, Key=file_path, Body=file_content)
    users_table = boto3.client('dynamodb', region_name=region)
    try:
        
        s3 = boto3.client('s3')
        csv_file = s3.get_object(Bucket = bucket_name, Key = 'sample.csv' )
        record_list = []
        record_list = (x.strip() for x in csv_file['Body'].read().decode('utf-8').split('\r\n'))
        csv_reader = csv.reader(record_list, delimiter=',', quotechar='"')
        headers = next(csv_reader)
        now = datetime.now()
        x = now.strftime("%m/%d/%Y, %H:%M:%S")
        y = str(uuid.uuid4())
        for row in csv_reader:
            UserName = row[0]
            users_table.put_item(
                TableName = "Users",
                Item = {
                    'ID': {'S' : y},  
                    'UserName' : {'S' : str(UserName)},
                    'DateTime' : {'S' : x}
                })
    
    except Exception as e:
        print(str(e))
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success! Users in CSV uploaded to DynamoDB.')
    }