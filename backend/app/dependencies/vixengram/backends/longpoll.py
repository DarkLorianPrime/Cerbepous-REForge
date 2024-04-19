import asyncio
from typing import List

from pydantic import TypeAdapter

from dependencies.pydantic_models.telegram_objects import Message
from dependencies.vixengram.aiohttpx import client
from dependencies.vixengram.settings import core_logger
from utils.url import url_compiler


class LongPoll:
    def __init__(self):
        core_logger.warning("Longpoll method is not optimal and optimized for telegram, please, "
                            "use webhooks (callback). With this method VixenApiDoc does not available.")
        self.actual_update_id = None
        self.update_url = url_compiler('getUpdates')

    async def get_updates(self):
        response = await client.get(self.update_url, params={"offset": self.actual_update_id})
        result = response.json()

        if not result["ok"]:
            raise RuntimeError(f"Longpoll return specified response (error): {result['description']}")

        return response.json()["result"]

    async def listen(self):
        await asyncio.sleep(3)
        result = await self.get_updates()

        if not result:
            return

        last_message = result[-1]
        update_id = last_message["update_id"]

        self.actual_update_id = update_id + 1
        ta = TypeAdapter(List[Message])
        return ta.validate_python(result)
