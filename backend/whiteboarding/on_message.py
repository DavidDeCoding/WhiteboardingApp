import boto3
import os
import json

WHITEBOARDING_TABLE = os.environ['WHITEBOARDING_TABLE']
db_client = boto3.resource('dynamodb')
table = db_client.Table(WHITEBOARDING_TABLE)


def handler(event, context):
    print(f"Event: {event}, Context: {context}")

    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    endpoint_url = f"https://{domain}/{stage}"
    client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)

    connection_id = event["requestContext"]["connectionId"]
    body = json.loads(event["body"])

    response = table.get_item(
        Key={'whiteboardId': "123"}
    )
    print(response)

    if "Item" in response:
        for user in response['Item']['users']:
            if user == connection_id:
                continue
            client.post_to_connection(
                ConnectionId=user,
                Data=body["message"]
            )

    return {"statusCode": 200}
