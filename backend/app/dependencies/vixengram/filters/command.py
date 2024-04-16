import operator
from typing import Optional, List

from dependencies.vixengram.filters.base import FilterObject


class CommandFilter(FilterObject):
    def __init__(self, commands: Optional[List[str]] = None, command: Optional[str] = None):
        super().__init__("message.text")
        prefix = "/"

        if command is not None:
            self.value = f"{prefix}{command}"
            self.operator = operator.eq

        elif commands is not None:
            self.value = [f"{prefix}{cmd}" for cmd in commands]
            self.operator = operator.contains

        else:
            raise ValueError("'command' or 'commands' must be provided.")