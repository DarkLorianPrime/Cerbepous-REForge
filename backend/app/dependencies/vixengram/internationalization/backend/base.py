import abc


class BaseLocalizationBackend(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def set_localization(self, chat_id: int, localization: str):
        raise NotImplementedError("Set localization is not implemented")

    @abc.abstractmethod
    async def get_localization(self, chat_id: int):
        raise NotImplementedError("Get localization is not implemented")

