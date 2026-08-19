import boto3

from app.core.config import settings


dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION
)

users_table = dynamodb.Table(settings.USERS_TABLE)
conversations_table = dynamodb.Table(settings.CONVERSATIONS_TABLE)
