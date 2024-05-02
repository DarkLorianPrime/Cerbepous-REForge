import json
from typing import Dict, List

from vixengram.keyboards.buttons import KeyboardButton


class CommonKeyboard:
    def __init__(self, resize_keyboard: bool = False):
        self.keyboard = []
        self.resize_keyboard = resize_keyboard

    async def row(self, *args: 'KeyboardButton') -> 'CommonKeyboard':
        buttons_list: List[Dict[str, str]] = []

        if len(args) > 4:
            raise AttributeError("The button should have no more than 4 arguments")

        for button in args:
            if not isinstance(button, KeyboardButton):
                raise AttributeError("Button instance must be a KeyboardButton")

            if button.callback_data is not None:
                raise AttributeError("Callback data is not supported from this keyboard type")

            buttons_list.append(
                {
                    "text": button.text,
                }
            )

        self.keyboard.append(buttons_list)
        return self

    async def get_keyboard(self):
        return json.dumps({"reply_keyboard": self.keyboard})
