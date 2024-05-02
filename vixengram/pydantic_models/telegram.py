import datetime
from typing import List, Dict

from pydantic import BaseModel, Field


class MessageChatInfo(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class MessageChatBody(MessageChatInfo):
    type: str


class MessageFromBody(MessageChatInfo):
    is_bot: bool
    language_code: str | None = None


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
    reply_markup: Dict[str, List[List[Dict[str, str]]]] | None = None
    chat_instance: str | None = None
    entities: List[EntitiesBody] | None = None


class Message(BaseModel):
    update_id: int
    message: MessageBody
    _command_args: str | None = None


class CallbackMessage(MessageBody):
    chat: MessageChatBody


class CallbackQuery(BaseModel):
    id: int
    from_: MessageFromBody = Field(..., alias="from")
    message: CallbackMessage
    _command_args: str | None = None
    data: str | None = None


class CallbackQueryEvent(BaseModel):
    update_id: int
    callback_query: CallbackQuery
