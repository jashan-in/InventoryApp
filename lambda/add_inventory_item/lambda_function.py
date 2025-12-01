import json
import boto3
from ulid import ULID

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        # Parse JSON body
        body = json.loads(event.get("body", "{}"))

        item_name = body.get("item_name")
        item_description = body.get("item_description")
        item_qty_on_hand = body.get("item_qty_on_hand")
        item_price = body.get("item_price")
        item_location_id = body.get("item_location_id")

        # Validate required fields
        if not all([item_name, item_description, item_qty_on_hand, item_price, item_location_id]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        # Generate ULID
        item_id = str(ULID())

        # Put into DynamoDB
        table.put_item(Item={
            "item_id": item_id,
            "item_name": item_name,
            "item_description": item_description,
            "item_qty_on_hand": int(item_qty_on_hand),
            "item_price": float(item_price),
            "item_location_id": int(item_location_id)
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item added", "item_id": item_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
