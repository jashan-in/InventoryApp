import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

def decimal_converter(o):
    if isinstance(o, Decimal):
        return float(o)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        # Get location id from URL path
        location_id = event["pathParameters"]["id"]

        # Query using the GSI
        response = table.query(
            IndexName="location-index",
            KeyConditionExpression=Key("item_location_id").eq(location_id)
        )

        return {
            "statusCode": 200,
            "body": json.dumps(response["Items"], default=decimal_converter)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
