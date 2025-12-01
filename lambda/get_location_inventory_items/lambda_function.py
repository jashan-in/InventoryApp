import json
import boto3
from boto3.dynamodb.conditions import Attr
import json
from decimal import Decimal

def decimal_converter(o):
    if isinstance(o, Decimal):
        return float(o)


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        location_id = int(event["pathParameters"]["id"])

        # Scan and filter by sort key
        response = table.scan(
            FilterExpression=Attr("item_location_id").eq(location_id)
        )

        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=decimal_converter)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
