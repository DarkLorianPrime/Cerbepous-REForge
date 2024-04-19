import operator
from typing import Optional, List

from dependencies.pydantic_models.telegram_objects import Message
from dependencies.vixengram.filters.base import FilterObject


class CommandFilter(FilterObject):
    def __init__(self, commands: Optional[List[str] | str] = None):
        super().__init__("message.text")
        prefix = "/"

        self.need_args = True

        if isinstance(commands, list):
            self.value = [f"{prefix}{cmd.replace('/', '')}" for cmd in commands]
            self.operator = operator.contains

        elif isinstance(commands, str):
            self.value = f"{prefix}{commands.replace('/', '')}"
            self.operator = lambda x, y: x in y

        else:
            raise ValueError("'command' or 'commands' must be provided.")


class CommandArguments:
    def __init__(self, input_object: Message):
        self.argument = input_object._command_args
