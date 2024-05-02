from vixengram.api import BotAPI
from vixengram.filters.base import F
from vixengram.internationalization import ProxyLanguage
from vixengram.keyboards.buttons import KeyboardButton
from vixengram.keyboards.inline_keyboard import InlineKeyboard
from vixengram.routing import Router

router = Router(
    title="Help Router"
)


async def generate_help_kb(lang: ProxyLanguage):
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

    return kb


@router.message(F.data == "help_menu")
async def open_help_menu(bot: BotAPI, lang: ProxyLanguage):
    await bot.edit_message(text=await lang("common.help_menu"), reply_markup=await generate_help_kb(lang))


@router.message(F.data == "help_who")
async def help_menu_button_who(bot: BotAPI, lang: ProxyLanguage):
    await bot.edit_message(text=await lang("help.text.who"), reply_markup=await generate_help_kb(lang))


@router.message(F.data == "help_start")
async def help_menu_button_start(bot: BotAPI, lang: ProxyLanguage):
    await bot.edit_message(text=await lang("help.text.start"), reply_markup=await generate_help_kb(lang))


@router.message(F.data == "help_about_me")
async def help_menu_button_about_me(bot: BotAPI, lang: ProxyLanguage):
    await bot.edit_message(text=await lang("help.text.aboutme"), reply_markup=await generate_help_kb(lang))


@router.message(F.data == "help_about_creator")
async def help_menu_button_creator(bot: BotAPI, lang: ProxyLanguage):
    await bot.edit_message(text=await lang("help.text.creator"), reply_markup=await generate_help_kb(lang))


@router.message(F.data == "help_mediasoft")
async def help_menu_button_mediasoft(bot: BotAPI, lang: ProxyLanguage):
    await bot.answer(text=await lang("common.mediasoft_info"))


@router.message(F.data == "help_exit")
async def help_menu_button_exit(bot: BotAPI, lang: ProxyLanguage):
    await bot.edit_message(text=await lang("help.exit"))