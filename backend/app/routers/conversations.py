import uuid
from datetime import datetime, timezone

from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, Depends, HTTPException, status

from app.database.dynamodb import conversations_table
from app.dependencies.auth import get_current_user
from app.models.conversation import (
    ConversationCreate,
    ConversationRename,
    MessageCreate
)


router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"]
)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def get_user_conversation(conversation_id: str, user_id: str):
    response = conversations_table.get_item(
        Key={"conversation_id": conversation_id}
    )

    conversation = response.get("Item")

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if conversation["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return conversation


@router.post("")
def create_conversation(
    request: ConversationCreate,
    current_user=Depends(get_current_user)
):
    conversation_id = str(uuid.uuid4())
    now = utc_now()

    conversation = {
        "conversation_id": conversation_id,
        "user_id": current_user["user_id"],
        "title": request.title,
        "messages": [],
        "created_at": now,
        "updated_at": now
    }

    conversations_table.put_item(Item=conversation)
    return conversation


@router.get("")
def get_conversations(current_user=Depends(get_current_user)):
    response = conversations_table.query(
        IndexName="user_id-index",
        KeyConditionExpression=Key("user_id").eq(
            current_user["user_id"]
        )
    )

    conversations = response.get("Items", [])

    result = [
        {
            "conversation_id": item["conversation_id"],
            "title": item["title"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"]
        }
        for item in conversations
    ]

    result.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return result


@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: str,
    current_user=Depends(get_current_user)
):
    return get_user_conversation(
        conversation_id,
        current_user["user_id"]
    )


@router.post("/{conversation_id}/messages")
def add_message(
    conversation_id: str,
    request: MessageCreate,
    current_user=Depends(get_current_user)
):
    get_user_conversation(
        conversation_id,
        current_user["user_id"]
    )

    message = {
        "message_id": str(uuid.uuid4()),
        "role": request.role,
        "content": request.content,
        "created_at": utc_now()
    }

    now = utc_now()

    conversations_table.update_item(
        Key={"conversation_id": conversation_id},
        UpdateExpression=(
            "SET messages = list_append("
            "if_not_exists(messages, :empty), :message"
            "), updated_at = :updated_at"
        ),
        ExpressionAttributeValues={
            ":empty": [],
            ":message": [message],
            ":updated_at": now
        },
        ReturnValues="ALL_NEW"
    )

    return message


@router.put("/{conversation_id}")
def rename_conversation(
    conversation_id: str,
    request: ConversationRename,
    current_user=Depends(get_current_user)
):
    get_user_conversation(
        conversation_id,
        current_user["user_id"]
    )

    response = conversations_table.update_item(
        Key={"conversation_id": conversation_id},
        UpdateExpression="SET title = :title, updated_at = :updated_at",
        ExpressionAttributeValues={
            ":title": request.title,
            ":updated_at": utc_now()
        },
        ReturnValues="ALL_NEW"
    )

    return response["Attributes"]


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    current_user=Depends(get_current_user)
):
    get_user_conversation(
        conversation_id,
        current_user["user_id"]
    )

    conversations_table.delete_item(
        Key={"conversation_id": conversation_id}
    )

    return {"message": "Conversation deleted"}
