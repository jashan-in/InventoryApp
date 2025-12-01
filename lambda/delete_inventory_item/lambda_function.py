import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        item_id = event["pathParameters"]["id"]

        # Check if item exists
        check = table.get_item(Key={"item_id": item_id})
        if "Item" not in check:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }

        # Delete
        table.delete_item(Key={"item_id": item_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item deleted successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
