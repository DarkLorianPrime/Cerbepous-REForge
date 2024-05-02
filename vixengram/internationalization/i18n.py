import logging
import os
import re
from collections import defaultdict
from typing import List, Dict, Type
from shutil import copy

from vixengram.pydantic_models.telegram import Message
from vixengram.internationalization.backend.base import (
    BaseLocalizationBackend,
)
from vixengram.internationalization.backend.session import SessionBackend
from vixengram.settings import i18n_logger

ABSOLUTE_DEFAULT_PATH = "dependencies/vixengram/internationalization"
REGEX_FILENAME = r"(?P<lang>[a-z]{0,2}\_[A-Z]{0,2})\.lang"
file_regex = re.compile(REGEX_FILENAME)


class I18N:
    def create_localization_folder(self):
        os.makedirs("./lang/", exist_ok=True)
        if "ru_RU.lang" not in os.listdir("./lang/"):
            copy(f"{ABSOLUTE_DEFAULT_PATH}/examples/ru_RU.lang", "./lang/")

        if "en_US.lang" not in os.listdir("./lang/"):
            copy(f"{ABSOLUTE_DEFAULT_PATH}/examples/en_US.lang", "./lang/")

    def read_localization(self, path: str):
        with open(path, "r") as local_file:
            lang: re.Match[str] | None = file_regex.search(path)
            local_name: str = lang.group(1) if lang is not None else "undefined"
            for line in local_file.readlines():
                try:
                    key, value = line.split("=", maxsplit=1)
                    self.localizations[local_name][key] = value.rstrip()
                except ValueError:
                    if not self.soft_load:
                        raise
                    else:
                        logging.warning("Unable to load some localizations")

    def read_localizations(self):
        for language_files in os.listdir("./lang/"):
            self.read_localization(f"./lang/{language_files}")

    def get_text(self, localization: str | None = None, code: str | None = None):
        if localization is None:
            localization = self.default_language

        return self.localizations[localization].get(code)

    def __call__(
        self,
        backend: Type[BaseLocalizationBackend] | None = None,
        language_list: List[Dict[str, str]] | None = None,
        default_language: str = "ru_RU",
        soft_load: bool = False,
    ):
        self.languages = language_list
        self.default_language: str = default_language
        self.backend = (
            backend(default_language)
            if backend is not None
            else SessionBackend(default_language)
        )
        self.soft_load: bool = soft_load
        self.localizations: defaultdict = defaultdict(dict)
        self.create_localization_folder()
        self.read_localizations()
        return self

    async def set_localization(self, chat_id: int, language: str):
        await self.backend.set_localization(chat_id, language)


class ProxyLanguage:
    def __init__(self, input_object: Message):
        self.i18n: I18N = i18n
        self.chat_id: int = input_object.message.chat.id

    async def __call__(self, unlocalized_text: str, force_code: str | None = None):
        localization_lang: str = (
            await self.i18n.backend.get_localization(self.chat_id)
            if force_code is None
            else force_code
        )
        result = self.i18n.get_text(
            localization=localization_lang, code=unlocalized_text
        )
        if result is None:
            result = self.i18n.get_text(code=unlocalized_text)
            i18n_logger.critical(
                f"Could not load '{unlocalized_text}' from '{localization_lang}' locale. "
                f"Using default."
            )

        return result


i18n = I18N()
