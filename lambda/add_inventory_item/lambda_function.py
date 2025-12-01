import boto3
import json
import uuid
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")  # DynamoDB table name

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"], parse_float=Decimal)

        required_fields = ["item_name", "item_description", "item_qty_on_hand", "item_price", "item_location_id"]
        if not all(field in body for field in required_fields):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        item_id = str(uuid.uuid4())

        item = {
            "item_id": item_id,
            "item_name": body["item_name"],
            "item_description": body["item_description"],
            "item_qty_on_hand": int(body["item_qty_on_hand"]),
            "item_price": Decimal(str(body["item_price"])),
            "item_location_id": int(body["item_location_id"])
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item added", "item_id": item_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
