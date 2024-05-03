from importlib.util import find_spec
from typing import Any, Dict, List

from vixengram.api import TelegramAPI
from vixengram.backends.webhooks import WebHook, delete_webhook
from vixengram.internationalization.i18n import I18N
from vixengram.backends.longpoll import LongPoll
from vixengram.pydantic_models.telegram import CallbackQueryEvent, CallbackQuery, Message
from vixengram.routing import Router
from vixengram.settings import routing_logger
from vixengram.vixenapi.core import VixenAPIGenerator
from aiohttp import web

from vixengram.settings import settings as private_settings


class VixenGram:
    def __init__(
            self,
            token: str,
            title: str = "Example App",
            version: str = "0.0.1",
            i18n: I18N | None = None,
    ):
        self.api_json = None
        self.title: str = title
        self.version: str = version
        self.__token: str = token
        private_settings.TG_TOKEN = token
        self.i18n: I18N | None = i18n
        self.__main_router: Router | None = None
        self.api = TelegramAPI()

    async def webhook(
            self,
            host: str,
            port: int,
            webhook_url: str,
            api_schema: dict | None = None
    ) -> None:
        wh = WebHook(webhook_url)
        await wh.set_webhook()

        if not isinstance(self.__main_router, Router):
            raise AttributeError("Main router need `Router` type.")

        wh.app["main_router"] = self.__main_router
        wh.app["api_schema"] = api_schema
        await web._run_app(wh.app, host=host, port=port)
        delete_webhook()

    async def polling(self) -> None:
        """
        Telegram LongPoll Method to Get Updates
        """
        lp = LongPoll()

        while True:
            messages = await lp.listen()

            if not messages:
                continue

            if not isinstance(self.__main_router, Router):
                raise AttributeError("Main router need `Router` type.")

            message: CallbackQuery | CallbackQueryEvent | Message
            for message in messages:
                if isinstance(message, CallbackQueryEvent):
                    message = message.callback_query

                routing_logger.info(
                    "ACCESS: %s - chat_id: %s",
                    message.message.date.strftime("%Y-%m-%d %H:%M:%S"),
                    message.message.chat.id,
                )
                await self.__main_router.call_handler(message)

    def add_router(self, router: Router) -> None:
        self.__main_router = router

    def generate_api(self) -> Dict[str, Dict[str, Any] | List[Dict[str, Any]] | str]:
        if not isinstance(self.__main_router, Router):
            raise AttributeError("Main router need `Router` type.")

        jinja2 = find_spec("jinja2")
        aiohttp = find_spec("aiohttp")

        if not all((jinja2, aiohttp)):
            raise ModuleNotFoundError(
                "Package Jinja2 or aiohttp not found. The Docs API cannot be generated."
            )

        return VixenAPIGenerator(
            self.title, self.version, routers=self.__main_router.get_routers()
        ).generate_json()
