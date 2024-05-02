from vixengram.api import BotAPI
from vixengram.filters.base import F
from vixengram.internationalization import i18n, ProxyLanguage
from vixengram.routing import Router
from vixengram.types.telegram_type import MessageObject

router = Router(
    title="Translate Router"
)


@router.message(F.data == "lang_to_ru")
async def change_to_ru(bot: BotAPI, message: MessageObject, lang: ProxyLanguage):
    await i18n.set_localization(message.chat.id, "ru_RU")
    await bot.answer(await lang("translate.change_language"))


@router.message(F.data == "lang_to_en")
async def change_to_en(bot: BotAPI, message: MessageObject, lang: ProxyLanguage):
    await i18n.set_localization(message.chat.id, "en_US")
    await bot.answer(await lang("translate.change_language"))
