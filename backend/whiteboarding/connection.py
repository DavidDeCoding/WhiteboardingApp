import boto3
import os

WHITEBOARDING_TABLE = os.environ['WHITEBOARDING_TABLE']
db_client = boto3.resource('dynamodb')
table = db_client.Table(WHITEBOARDING_TABLE)


def handler(event, context):
    print(f"Event: {event}, Context: {context}")

    event_type = event["requestContext"]["eventType"]

    if event_type == "CONNECT":
        print(f"Connected: {event['requestContext']['connectionId']}")

        response = table.get_item(
            Key={'whiteboardId': "123"}
        )
        print(response)

        if "Item" not in response:
            table.put_item(
                Item={
                    'whiteboardId': "123",
                    'users': [event['requestContext']['connectionId']]
                }
            )
        else:
            response['Item']['users'].append(event['requestContext']['connectionId'])
            table.update_item(
                Key={'whiteboardId': "123"},
                ExpressionAttributeNames={'#users': 'users'},
                ExpressionAttributeValues={
                    ':users': response['Item']['users']
                },
                UpdateExpression="SET #users = :users"
            )

    elif event_type == "DISCONNECT":
        print(f"Disconnected: {event['requestContext']['connectionId']}")
        response = table.get_item(
            Key={'whiteboardId': "123"}
        )
        print(response)

        response['Item']['users'].remove(event['requestContext']['connectionId'])
        table.update_item(
            Key={'whiteboardId': "123"},
            ExpressionAttributeNames={'#users': 'users'},
            ExpressionAttributeValues={
                ':users': response['Item']['users']
            },
            UpdateExpression="SET #users = :users"
        )

    else:
        print(f"Unknown eventType: {event_type}")

    return {"statusCode": 200}

