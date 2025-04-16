import json
import boto3
import random
from decimal import Decimal

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
# define tables one at a table per action later

def lambda_handler(event, context):
    # Handle CORS preflight request
    if event['routeKey'] == "OPTIONS /items":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "https://didyakno.com",
                "Access-Control-Allow-Methods": "OPTIONS",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    # handle actual fun fact get
    body = {}
    statusCode = 200
    headers = {
        "Content-Type": "application/json"
    }

    try:
        table1 = dynamodb.Table('tblFunFacts')
        tableName = 'tblFunFacts'
        if event['routeKey'] == "GET /items":
            body = table1.get_item(
                Key={'Fact ID': str(random.randint(1, 750))})
            body = body["Item"]
            responseBody = [
                {'Fact #': body['Fact ID'], 'Fact': body['Fact']}]

            # if successful, update count in table2
            table2 = dynamodb.Table('tblFunFactsCounter')
            tableName = 'tblFunFactsCounter'
            response = table2.update_item(
                Key={'Count ID': '0'},
                UpdateExpression='SET factCount = factCount + :val',
                ExpressionAttributeValues={':val': 1},
                ReturnValues="UPDATED_NEW")
            # Update responseBody list with new count
            responseBody.append({'factCount': int(response['Attributes']['factCount'])})
            # Return json to client
            body = json.dumps(responseBody)
            body = responseBody
    except KeyError:
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
    body = json.dumps(body)
    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "https://didyakno.com",
            "Access-Control-Allow-Methods": "OPTIONS",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": body
    }
    return res