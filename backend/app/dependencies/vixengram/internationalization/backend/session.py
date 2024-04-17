import abc

from dependencies.vixengram.internationalization.backend.base import BaseLocalizationBackend


class SessionBackend(BaseLocalizationBackend, metaclass=abc.ABCMeta):
    """
    WARNING: После перезагрузки python - все данные будут очищены!
    """
    def __init__(self, default_locale: str):
        super().__init__(default_locale)
        self.storage = {}

    def get_localization(self, chat_id: int):
        local = self.storage.get(chat_id)
        if local is None:
            self.set_localization(chat_id, self.default_locale)

        return self.storage.get(chat_id)

    def set_localization(self, chat_id: int, localization: str):
        self.storage[chat_id] = localization
