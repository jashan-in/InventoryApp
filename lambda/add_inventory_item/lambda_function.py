import json
import uuid
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        # Extract fields from request body
        item_name = body.get("item_name")
        item_description = body.get("item_description")
        item_qty_on_hand = body.get("item_qty_on_hand")
        item_price = body.get("item_price")
        item_location_id = body.get("item_location_id")

        # Validate required fields
        if not item_name or item_qty_on_hand is None or item_location_id is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        # Generate UUID for item_id
        item_id = str(uuid.uuid4())

        # Insert into DynamoDB
        table.put_item(
            Item={
                "item_id": item_id,
                "item_location_id": item_location_id,
                "item_name": item_name,
                "item_description": item_description,
                "item_qty_on_hand": item_qty_on_hand,
                "item_price": item_price,
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item added successfully",
                "item_id": item_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
