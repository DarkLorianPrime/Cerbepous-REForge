import logging

from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)
i18n_logger = logging.getLogger("vixengram_i18n")
core_logger = logging.getLogger("vixengram_core")
api_logger = logging.getLogger("vixengram_api")
routing_logger = logging.getLogger("vixengram_routing")
debug_logger = logging.getLogger("vixengram_debug")


class VixengramSettings(BaseSettings):
    TG_TOKEN: str | None = None
    api_url: str = "https://api.telegram.org"


settings = VixengramSettings()
