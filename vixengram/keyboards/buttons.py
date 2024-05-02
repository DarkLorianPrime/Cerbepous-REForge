

class KeyboardButton:
    def __init__(
            self,
            text: str,
            callback_data: str = None,
    ):
        self.text = text
        self.callback_data = callback_data
