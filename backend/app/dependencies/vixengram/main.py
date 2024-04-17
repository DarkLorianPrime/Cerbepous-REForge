from dependencies.vixengram.api import TelegramAPI
from dependencies.vixengram.longpoll import LongPoll
from dependencies.vixengram.routing import Router
from settings import settings


class VixenGram:
    def __init__(self, token: str = None):
        self.__token = token or settings.TG_TOKEN
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
                await self.__main_router.call_handler(message)

    def add_router(self, router: 'Router'):
        self.__main_router = router
