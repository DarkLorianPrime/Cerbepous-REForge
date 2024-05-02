from vixengram.pydantic_models.telegram import Message


class MessageObject:
    def __init__(self, message: Message):
        self.message = message.message

    def __getattr__(self, item):
        return self.message[item]
