import atexit

import aiohttp_jinja2
import jinja2
from aiohttp import web
import re

from aiohttp.web_request import Request
from vixengram.aiohttpx import client, sync_client
from vixengram.pydantic_models.telegram import Message, CallbackQueryEvent

from vixengram.utils.url import url_compiler

from vixengram.settings import routing_logger

get_path = re.compile(r"([^/?]+)(?=\?|$)")


@atexit.register
def delete_webhook():
    webhook_url = url_compiler("deleteWebhook")
    sync_client.post(webhook_url)


class WebHook:
    def __init__(self, webhook_url: str):
        self.__webhook_url = webhook_url
        self.app = web.Application()
        path = get_path.search(webhook_url)
        route_path = "/" + "" if path is None else path.group(1)
        self.app.router.add_post(route_path, self.webhook_handler)
        self.app.router.add_get("/docs", self.vixenapi_handler)
        aiohttp_jinja2.setup(self.app, enable_async=True,
                             loader=jinja2.PackageLoader("vixengram", "vixenapi/templates"))

    async def set_webhook(self):
        webhook_url = url_compiler("setWebhook")
        await client.post(webhook_url, params={"url": self.__webhook_url})

    async def json_to_pydantic(self, json_object: dict):
        if json_object.get("callback_query"):
            return CallbackQueryEvent.model_validate(json_object)

        return Message.model_validate(json_object)

    async def webhook_handler(self, request: Request) -> web.Response:
        message_json = await request.json()
        message = await self.json_to_pydantic(message_json)

        if hasattr(message, "callback_query"):
            message = message.callback_query

        routing_logger.info(
            "ACCESS: %s - chat_id: %s",
            message.message.date.strftime("%Y-%m-%d %H:%M:%S"),
            message.message.chat.id,
        )
        await request.app["main_router"].call_handler(message)
        return web.Response(status=200)

    async def vixenapi_handler(self, request: Request) -> web.Response:
        response = await aiohttp_jinja2.render_template_async(
            'documentation.jinja2',
            request,
            self.app["api_schema"]
        )
        return response
