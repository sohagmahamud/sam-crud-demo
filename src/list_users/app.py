import os
import json
import boto3
from botocore.paginate import TokenEncoder

def lambda_handler(event, context):
    key= event['key'] 
    client = boto3.client('dynamodb', region_name='ap-southeast-1')
    
    if not key:
        pagination_config = {"MaxItems": 20, "PageSize": 5}
    else:
        encoder = TokenEncoder()
        encoded_token=encoder.encode({'ExclusiveStartKey':  {'id': {'S': key}}})
        pagination_config = {"MaxItems": 20, "PageSize": 5, "StartingToken":  encoded_token } 
        

    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        TableName="Users", 
        PaginationConfig=pagination_config
    )
            
    for page in response_iterator:
        Items = page['Items']
    
    print(Items)
    print("LastEvaluatedKey")
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(Items),
        'LastEvaluatedKey' : page["LastEvaluatedKey"]
    }