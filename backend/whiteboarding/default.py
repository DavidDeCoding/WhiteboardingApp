
def handler(event, context):
    print(f"Event: {event}, Context: {context}")
    return {"statusCode": 200}
