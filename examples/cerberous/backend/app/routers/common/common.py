from vixengram.internationalization.i18n import ProxyLanguage

from routers.common.urls import Urls
from vixengram.api import BotAPI
from vixengram.filters.command import CommandFilter
from vixengram.keyboards.buttons import KeyboardButton
from vixengram.keyboards.inline_keyboard import InlineKeyboard
from vixengram.routing import Router
from vixengram.types.telegram_type import MessageObject

router = Router(
    title="Common router",
)


@router.message(CommandFilter(["кто", "who"]))
async def who_me(bot: BotAPI, message: MessageObject):
    string = f"Я думаю, ты - {message.from_.first_name} {message.from_.last_name}, бяка!"
    await bot.answer(string)


@router.message(CommandFilter("start"))
async def start(bot: BotAPI, lang: ProxyLanguage):
    await bot.send_animation(animation_url=Urls.animation_url)
    await bot.answer(await lang("common.start_text"))


@router.message(CommandFilter("help"))
async def help_menu(bot: BotAPI, lang: ProxyLanguage):
    kb = InlineKeyboard()
    await kb.row(KeyboardButton(await lang("common.open_help_menu"), "help_menu"))
    await kb.row(
        KeyboardButton(await lang("common.help_ru"), "lang_to_ru"),
        KeyboardButton(await lang("common.help_en"), "lang_to_en")
    )
    await bot.answer(text=await lang("common.help_menu"), reply_markup=kb)


@router.message(CommandFilter("mediasoft"))
async def mediasoft_info(bot: BotAPI, lang: ProxyLanguage):
    await bot.answer(await lang("common.mediasoft_info"))
