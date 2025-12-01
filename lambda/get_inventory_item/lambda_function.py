import json
import boto3
from decimal import Decimal

def decimal_converter(o):
    if isinstance(o, Decimal):
        return float(o)
    raise TypeError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        # Read path parameter ID
        item_id = event["pathParameters"]["id"]

        # Query DynamoDB
        response = table.get_item(Key={"item_id": item_id})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }

        # Convert DynamoDB Decimal values → float
        item = json.loads(json.dumps(response["Item"], default=decimal_converter))

        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
