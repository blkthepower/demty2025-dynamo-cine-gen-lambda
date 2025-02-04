import os
from typing import List, Dict

import boto3


target_table_name = os.environ["TARGET_TABLE_NAME"]
region = os.environ["REGION"]
dynamodb = boto3.resource("dynamodb", region_name=region)


def lambda_handler(event, context):
    try:
        table = dynamodb.Table(target_table_name)
        insert_items(table, event)
        
        return {
            "statusCode": 200,
            "body": {
                "message": "Items inserted successfully",
                "items": event
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {
                "message": "Error inserting items",
                "error": str(e)
            }
        }


def insert_items(table, items: List[Dict]) -> None:
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)