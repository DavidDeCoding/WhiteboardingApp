import boto3


def handler(event, context):
    print(f"Event: {event}, Context: {context}")

    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    endpoint_url = f"https://{domain}/{stage}"
    client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)

    connection_id = event["requestContext"]["connectionId"]
    client.post_to_connection(
        ConnectionId=connection_id,
        Data="Hello"
    )
    return {"statusCode": 200}
