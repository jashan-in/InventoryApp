import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        # Force everything to STRING except numeric qty and price
        item = {
            "item_id": str(uuid.uuid4()),
            "item_name": body["item_name"],
            "item_description": body["item_description"],
            "item_qty_on_hand": Decimal(str(body["item_qty_on_hand"])),
            "item_price": Decimal(str(body["item_price"])),
            "item_location_id": str(body["item_location_id"])  # <-- FIX HERE
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item added", "item_id": item["item_id"]})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
