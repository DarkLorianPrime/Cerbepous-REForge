from dependencies.pydantic_models.telegram_objects import Message
from dependencies.vixengram.aiohttpx import client
from utils.url import url_compiler


class LongPoll:
    def __init__(self):
        self.actual_update_id = None
        self.update_url = url_compiler('getUpdates')

    async def get_updates(self):
        response = await client.get(self.update_url, params={"offset": self.actual_update_id})
        result = response.json()

        if not result["ok"]:
            raise RuntimeError(f"Longpoll return specified response (error): {result['description']}")

        return response.json()["result"]

    async def listen(self):
        result = await self.get_updates()

        if not result:
            return

        last_message = result[0]
        update_id = last_message["update_id"]

        self.actual_update_id = update_id + 1
        return Message.model_validate(result[0])
