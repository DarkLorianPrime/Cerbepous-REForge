from vixengram.internationalization.i18n import ProxyLanguage

from examples.cerberous.backend.app.routers.common.texts import Texts
from vixengram.api import BotAPI, TelegramAPI
from vixengram.filters.command import CommandFilter
from vixengram.keyboards.buttons import KeyboardButton
from vixengram.keyboards.inline_keyboard import InlineKeyboard
from vixengram.routing import Router
from vixengram.types.telegram_type import MessageObject

router = Router(
    title="Common router",
)


@router.message(CommandFilter("кто"))
async def who_me(bot: BotAPI, message: MessageObject):
    string = f"Я думаю, ты - {message.from_.first_name} {message.from_.last_name}, бяка!"
    await bot.answer(string)


@router.message(CommandFilter("start"))
async def start(bot: BotAPI, lang: ProxyLanguage):
    await bot.send_animation(animation_url=Texts.animation_url)
    await bot.answer(await lang("common.start_text"))


@router.message(CommandFilter("help"))
async def help_menu(bot: BotAPI):
    kb = InlineKeyboard()
    await kb.row(KeyboardButton("Open help", "help_menu"))
    await bot.answer(text="Help menu:", reply_markup=kb)


@router.message(CommandFilter("mediasoft"))
async def mediasoft_info(bot: BotAPI, lang: ProxyLanguage):
    await bot.answer(await lang("common.mediasoft_info"))