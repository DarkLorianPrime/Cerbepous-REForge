from typing import Any

from dependencies.pydantic_models.telegram_objects import Message
from dependencies.vixengram.aiohttpx import client
from dependencies.vixengram.settings import api_logger
from utils.url import url_compiler


class TelegramAPI:
    def __init__(self, method: str | None = None) -> None:
        self.__method = method

    def __getattr__(self, method: str) -> "TelegramAPI":
        return TelegramAPI(method)

    async def __call__(self, *args, **kwargs) -> Any:
        if self.__method is None:
            raise Exception("Method not passed")

        url: str = url_compiler(self.__method)
        response = await client.get(url, params=kwargs)
        api_logger.debug("API response: %s", response)
        return response.json()


class BotAPI:
    def __init__(self, message_object: Message) -> None:
        self.__message = message_object.message
        self.__api = TelegramAPI()

    async def answer(self, text: str) -> None:
        await self.__api.sendMessage(chat_id=self.__message.chat.id, text=text)

    async def reply(self, text: str, reply_message_id: int | None = None) -> None:
        if reply_message_id is None:
            reply_message_id = self.__message.message_id

        await self.__api.sendMessage(
            chat_id=self.__message.chat.id,
            text=text,
            reply_to_message_id=reply_message_id,
        )
