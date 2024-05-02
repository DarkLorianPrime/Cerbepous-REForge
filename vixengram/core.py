from importlib.util import find_spec

from vixengram.api import TelegramAPI
from vixengram.internationalization.i18n import I18N
from vixengram.backends.longpoll import LongPoll
from vixengram.routing import Router
from vixengram.settings import routing_logger
from vixengram.vixenapi.core import VixenAPIGenerator

from vixengram.settings import settings as private_settings


class VixenGram:
    def __init__(
        self,
        token: str,
        title: str = "Example App",
        version: str = "0.0.1",
        i18n: I18N | None = None,
    ):
        self.title: str = title
        self.version: str = version
        self.__token: str = token
        private_settings.TG_TOKEN = token
        self.i18n: I18N | None = i18n
        self.__main_router: Router | None = None
        self.api = TelegramAPI()

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

            for message in messages:
                if hasattr(message, "callback_query"):
                    message = message.callback_query

                routing_logger.info(
                    "ACCESS: %s - chat_id: %s",
                    message.message.date.strftime("%Y-%m-%d %H:%M:%S"),
                    message.message.chat.id,
                )
                await self.__main_router.call_handler(message)

    def add_router(self, router: Router) -> None:
        self.__main_router = router

    def generate_api(self) -> None:
        if not isinstance(self.__main_router, Router):
            raise AttributeError("Main router need `Router` type.")

        jinja2 = find_spec("jinja2")
        aiohttp = find_spec("aiohttp")

        if not all((jinja2, aiohttp)):
            # raise ModuleNotFoundError(
            "Package Jinja2 or aiohttp not found. The Docs API cannot be generated."
        # )

        VixenAPIGenerator(
            self.title, self.version, routers=self.__main_router.get_routers()
        ).generate_json()
