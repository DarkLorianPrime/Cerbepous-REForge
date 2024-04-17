from dependencies.vixengram.api import TelegramAPI
from dependencies.vixengram.internationalization.i18n import I18N
from dependencies.vixengram.longpoll import LongPoll
from dependencies.vixengram.routing import Router
from dependencies.vixengram.settings import routing_logger

try:
    from settings import settings
except ImportError:
    from dependencies.vixengram.settings import settings


class VixenGram:
    def __init__(
            self,
            token: str = None,
            i18n: I18N = None
    ):
        self.__token = token or settings.TG_TOKEN
        self.i18n = i18n
        self.__main_router = None
        self.api = TelegramAPI()

    async def polling(self):
        """
        Telegram LongPoll Method to Get Updates
        """
        lp = LongPoll()
        while True:
            messages = await lp.listen()

            if not messages:
                continue

            if not isinstance(self.__main_router, Router):
                raise AttributeError('Main router need `Router` type.')

            for message in messages:
                routing_logger.info(
                    "ACCESS: %s - chat_id: %s",
                    message.message.date.strftime('%Y-%m-%d %H:%M:%S'),
                    message.message.chat.id
                )
                await self.__main_router.call_handler(message)

    def add_router(self, router: 'Router'):
        self.__main_router = router
