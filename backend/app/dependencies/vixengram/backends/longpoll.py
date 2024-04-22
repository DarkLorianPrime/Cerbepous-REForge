import asyncio
from typing import List, Dict, Any

from httpx import Response
from pydantic import TypeAdapter

from dependencies.pydantic_models.telegram_objects import Message
from dependencies.vixengram.aiohttpx import client
from utils.url import url_compiler


class LongPoll:
    def __init__(self) -> None:
        self.actual_update_id: int | None = None
        self.update_url = url_compiler("getUpdates")

    async def get_updates(self) -> List[Dict[str, Any]]:
        response: Response = await client.get(
            self.update_url, params={"offset": self.actual_update_id}
        )
        result: Any = response.json()

        if not result["ok"]:
            raise RuntimeError(
                f"Longpoll return specified response (error): {result['description']}"
            )

        return result["result"]

    async def listen(self) -> List[Message] | None:
        await asyncio.sleep(3)
        result: List[Dict[str, Any]] = await self.get_updates()

        if not result:
            return None

        last_message = result[-1]
        update_id = last_message["update_id"]

        self.actual_update_id = update_id + 1
        ta = TypeAdapter(List[Message])
        return ta.validate_python(result)
