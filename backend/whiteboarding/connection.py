import boto3
import os

WHITEBOARDING_TABLE = os.environ['WHITEBOARDING_TABLE']

db_client = boto3.client('dynamodb')


def handler(event, context):
    print(f"Event: {event}, Context: {context}")

    event_type = event["requestContext"]["eventType"]

    if event_type == "CONNECT":
        print(f"Connected: {event['requestContext']['connectionId']}")

    elif event_type == "DISCONNECT":
        print(f"Disconnected: {event['requestContext']['connectionId']}")

    else:
        print(f"Unknown eventType: {event_type}")

    return {"statusCode": 200}

