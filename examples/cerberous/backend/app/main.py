import asyncio

from settings import settings
from vixengram.api import BotAPI
from vixengram.filters.base import F
from vixengram.filters.command import CommandFilter, CommandArguments
from vixengram.internationalization import i18n, ProxyLanguage
from vixengram.keyboards.buttons import KeyboardButton
from vixengram.keyboards.common_keyboard import CommonKeyboard
from vixengram.keyboards.inline_keyboard import InlineKeyboard
from vixengram.routing import Router
from vixengram.core import VixenGram
from vixengram.types.telegram_type import MessageObject

app = VixenGram(token=settings.TG_TOKEN, i18n=i18n())
main_router = Router()


@main_router.message(F.message.text == "ru")
async def ru(bot: BotAPI, message: MessageObject, lang: ProxyLanguage):
    kb = InlineKeyboard()
    await kb.row(KeyboardButton(text="en", callback_data="asd"), KeyboardButton(text="ru", callback_data="das"))
    await bot.answer(await lang("global.example"), reply_markup=await kb.get_keyboard())


@main_router.message((F.message.text == "en"))
@main_router.message((F.message.text == "cry"))
async def en(bot: BotAPI, lang: ProxyLanguage):
    await bot.reply(await lang("global.example", "en_US"))


@main_router.message(CommandFilter("help"))
async def fr(bot: BotAPI, lang: ProxyLanguage, commands: CommandArguments):
    # logging.info(list(commands.argument))
    await bot.reply(await lang("global.example", "fr_FR"))


@main_router.message(F.data == "das")
async def asdasd(bot: BotAPI):
    await bot.reply("спасибо за использование нашего сервиса.")


if __name__ == "__main__":
    app.add_router(main_router)
    app.generate_api()
    asyncio.run(app.polling())
