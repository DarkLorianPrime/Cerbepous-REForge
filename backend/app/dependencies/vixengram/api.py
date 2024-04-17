from pydantic import BaseModel

from dependencies.vixengram.aiohttpx import client
from dependencies.vixengram.settings import api_logger
from utils.url import url_compiler


class TelegramAPI:
    def __init__(self, method: str | None = None):
        self.__method = method

    def __getattr__(self, method: str):
        return TelegramAPI(method)

    async def __call__(self, *args, **kwargs):
        if self.__method is None:
            raise Exception('Method not passed')

        url = url_compiler(self.__method)
        response = await client.get(url, params=kwargs)
        api_logger.debug('API response: %s', response)
        return response.json()


class BotAPI:
    def __init__(self, message_object: BaseModel):
        self.__message = message_object.message
        self.__api = TelegramAPI()

    async def answer(self, text: str):
        await self.__api.sendMessage(
            chat_id=self.__message.chat.id,
            text=text
        )

    async def reply(self, text: str, reply_message_id: int = None):
        if reply_message_id is None:
            reply_message_id = self.__message.message_id

        await self.__api.sendMessage(
            chat_id=self.__message.chat.id,
            text=text,
            reply_to_message_id=reply_message_id
        )
