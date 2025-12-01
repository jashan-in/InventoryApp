import json
import boto3
import json
from decimal import Decimal

def decimal_converter(o):
    if isinstance(o, Decimal):
        return float(o)


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        item_id = event["pathParameters"]["id"]

        response = table.get_item(Key={"item_id": item_id})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps(response["Item"])
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
