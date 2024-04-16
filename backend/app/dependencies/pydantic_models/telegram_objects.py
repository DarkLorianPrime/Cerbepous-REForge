import datetime
from typing import List

from pydantic import BaseModel, Field


class MessageChatInfo(BaseModel):
    id: int
    first_name: str = None
    last_name: str = None
    username: str = None


class MessageChatBody(MessageChatInfo):
    type: str


class MessageFromBody(MessageChatInfo):
    is_bot: bool
    language_code: str


class EntitiesBody(BaseModel):
    offset: int
    length: int
    type: str


class MessageBody(BaseModel):
    message_id: int
    from_: MessageFromBody = Field(..., alias="from")
    chat: MessageChatBody
    date: datetime.datetime
    text: str
    entities: List[EntitiesBody] | None = None


class Message(BaseModel):
    update_id: int
    message: MessageBody
