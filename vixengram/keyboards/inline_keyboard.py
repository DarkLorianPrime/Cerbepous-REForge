import json
from typing import Dict, List

from vixengram.keyboards.buttons import KeyboardButton


class InlineKeyboard:
    def __init__(self):
        self.keyboard = []

    async def row(self, *args: 'KeyboardButton') -> 'InlineKeyboard':
        buttons_list: List[Dict[str, str]] = []

        for button in args:
            if not isinstance(button, KeyboardButton):
                raise AttributeError("Button instance must be a KeyboardButton")

            if button.callback_data is None:
                raise AttributeError("Callback data is required from this keyboard type")

            buttons_list.append(
                {
                    "text": button.text,
                    "callback_data": button.callback_data
                }
            )

        self.keyboard.append(buttons_list)
        return self

    async def get_keyboard(self):
        return json.dumps({"inline_keyboard": self.keyboard})
