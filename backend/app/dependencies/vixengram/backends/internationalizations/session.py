import abc

from dependencies.vixengram.backends.internationalizations.base import BaseLocalizationBackend


class SessionBackend(BaseLocalizationBackend, metaclass=abc.ABCMeta):
    """
    WARNING: После перезагрузки python - все данные будут очищены!
    """
    def __init__(self):
        self.storage = {}

    def get_localization(self, chat_id: int):
        return self.storage.get(chat_id)

    def set_localization(self, chat_id: int, localization: str):
        self.storage[chat_id] = localization
