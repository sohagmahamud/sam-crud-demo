import boto3
import sys
import json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

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
    
    table = dynamodb.Table(table_name)

    queryCount = 1

    # make initial query
    response = client.scan(TableName = 'sam-crud-demo-table' , Select='ALL_ATTRIBUTES'|'COUNT', Limit = 10)

    # extract the results
    items = response['Items']
    for item in items:
        id = item['ID']
        userName = item['UserName']
        dateTime = item['DateTime']
        size = sys.getsizeof(item)
        print(str(queryCount) + ' - ' + id + ' - ' + userName + ' - ' + dateTime + ' - ' + str(size))

    queryCount += 1

    while 'LastEvaluatedKey' in response:
        print('-------------')        
        key = response['LastEvaluatedKey']
        response = table.query(KeyConditionExpression=Key('UserName'), ExclusiveStartKey=key, limit=10)
        items = response['Items']
        for item in items:
            userName = item['UserName']
            dateTime = item['DateTime']
            size = sys.getsizeof(item)
            print(str(queryCount) + ' - ' + userName + ' - ' + dateTime + ' - ' + str(size), limit=10)
        queryCount += 1
    print('-------------')

    return {
     'statusCode': 200,
     'headers': {},
     'body': json.dumps(response['Items'])
   }