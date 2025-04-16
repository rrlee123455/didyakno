import boto3
import json

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('tblFunFactsCounter')
tableName = 'tblFunFactsCounter'

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    # Handle CORS preflight request
    if event['routeKey'] == "OPTIONS /stats":
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

    try:
        if event['routeKey'] == "GET /stats":

            response = table.get_item(
                Key={
                    'Count ID': '0'
                }
            )
            factCount = response['Item']['factCount']
            factCount = int(factCount)
            return {
                'statusCode': 200,
                'body': json.dumps({'factCount': factCount})
            }

    except Exception as e:
        print(f"Error updating stat tracker: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }