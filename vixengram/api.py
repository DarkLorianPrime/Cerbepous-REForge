from typing import Any, Literal

from vixengram.keyboards.common_keyboard import CommonKeyboard
from vixengram.keyboards.inline_keyboard import InlineKeyboard
from vixengram.pydantic_models.telegram import Message
from vixengram.aiohttpx import client
from vixengram.settings import api_logger, debug_logger
from vixengram.utils.url import url_compiler


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

    async def answer(self, text: str, reply_markup: InlineKeyboard | CommonKeyboard = None) -> None:
        body = {
            "text": text,
            "chat_id": self.__message.chat.id
        }
        if reply_markup is not None:
            if isinstance(reply_markup, str):
                body["reply_markup"] = reply_markup
            else:
                body["reply_markup"] = await reply_markup.get_keyboard()
        debug_logger.critical(body)
        debug_logger.critical(await self.__api.sendMessage(**body))

    async def reply(self, text: str, reply_message_id: int | None = None) -> None:
        if reply_message_id is None:
            reply_message_id = self.__message.message_id

        await self.__api.sendMessage(
            chat_id=self.__message.chat.id,
            text=text,
            reply_to_message_id=reply_message_id,
        )

    async def send_animation(self, animation_url: str) -> None:
        await self.__api.sendAnimation(
            chat_id=self.__message.chat.id,
            animation=animation_url
        )