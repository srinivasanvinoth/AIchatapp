from pydantic import BaseModel, Field
from typing import Literal


class ConversationCreate(BaseModel):
    title: str = Field(default="New Chat", min_length=1, max_length=100)


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)
    role: Literal["user", "assistant"] = "user"


class ConversationRename(BaseModel):
    title: str = Field(min_length=1, max_length=100)
