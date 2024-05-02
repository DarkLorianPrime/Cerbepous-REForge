import abc
from typing import Dict

from vixengram.internationalization.backend.base import (
    BaseLocalizationBackend,
)


class SessionBackend(BaseLocalizationBackend, metaclass=abc.ABCMeta):
    """
    WARNING: После перезагрузки python - все данные будут очищены!
    """

    def __init__(self, default_locale: str) -> None:
        super().__init__(default_locale)
        self.storage: Dict[int, str] = {}

    async def get_localization(self, chat_id: int) -> str:
        local = self.storage.get(chat_id)
        if local is None:
            await self.set_localization(chat_id, self.default_locale)

        return self.storage.get(chat_id, "default")

    async def set_localization(self, chat_id: int, localization: str) -> None:
        self.storage[chat_id] = localization
