import boto3
import json
from decimal import Decimal
import ulid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        required = ["item_name", "item_description", "item_qty_on_hand", "item_price", "item_location_id"]
        if not all(field in body for field in required):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        # Convert all numeric fields to Decimal
        item_qty = Decimal(str(body["item_qty_on_hand"]))
        item_price = Decimal(str(body["item_price"]))
        item_loc = Decimal(str(body["item_location_id"]))

        item_id = str(ulid.new())

        item = {
            "item_id": item_id,
            "item_name": body["item_name"],
            "item_description": body["item_description"],
            "item_qty_on_hand": item_qty,
            "item_price": item_price,
            "item_location_id": item_loc
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
