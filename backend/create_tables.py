import boto3
from botocore.exceptions import ClientError


REGION = "ap-south-1"

dynamodb = boto3.client(
    "dynamodb",
    region_name=REGION
)


def create_users_table():
    try:
        dynamodb.create_table(
            TableName="Users",
            KeySchema=[
                {
                    "AttributeName": "user_id",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "user_id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "login_id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "email",
                    "AttributeType": "S"
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "login_id-index",
                    "KeySchema": [
                        {
                            "AttributeName": "login_id",
                            "KeyType": "HASH"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                },
                {
                    "IndexName": "email-index",
                    "KeySchema": [
                        {
                            "AttributeName": "email",
                            "KeyType": "HASH"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print("Users table created.")

    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceInUseException":
            print("Users table already exists.")
        else:
            raise


def create_conversations_table():
    try:
        dynamodb.create_table(
            TableName="Conversations",
            KeySchema=[
                {
                    "AttributeName": "conversation_id",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "conversation_id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "user_id",
                    "AttributeType": "S"
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "user_id-index",
                    "KeySchema": [
                        {
                            "AttributeName": "user_id",
                            "KeyType": "HASH"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print("Conversations table created.")

    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceInUseException":
            print("Conversations table already exists.")
        else:
            raise


if __name__ == "__main__":
    create_users_table()
    create_conversations_table()
