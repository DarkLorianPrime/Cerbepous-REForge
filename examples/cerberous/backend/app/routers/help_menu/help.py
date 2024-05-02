from vixengram.api import BotAPI
from vixengram.filters.base import F
from vixengram.internationalization import ProxyLanguage
from vixengram.keyboards.buttons import KeyboardButton
from vixengram.keyboards.inline_keyboard import InlineKeyboard
from vixengram.routing import Router

router = Router(
    title="Help Router"
)


@router.message(F.data == "help_menu")
async def open_help_menu(bot: BotAPI, lang: ProxyLanguage):
    kb = InlineKeyboard()
    await kb.row(
        KeyboardButton(text=await lang("help.menu.who"), callback_data="help_who"),
        KeyboardButton(text=await lang("help.menu.start"), callback_data="help_start"),
    )
    await kb.row(
        KeyboardButton(text=await lang("help.menu.creator"), callback_data="help_about_creator"),
        KeyboardButton(text=await lang("help.menu.about"), callback_data="help_about_me"),
    )
    await kb.row(
        KeyboardButton(text=await lang("help.menu.mediasoft"), callback_data="help_mediasoft"),
    )
    await kb.row(
        KeyboardButton(text=await lang("help.menu.exit"), callback_data="help_exit"),
    )

    await bot.answer(text=await lang("common.help_menu"), reply_markup=kb)
