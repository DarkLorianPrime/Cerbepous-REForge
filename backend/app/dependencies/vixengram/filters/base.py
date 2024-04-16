from typing import List, Tuple

from pydantic import BaseModel
import operator


class OperatorsMixin:
    def __generate_filter(self, operator_object: operator, other):
        self.operator = operator_object
        self.value = other
        return self

    def __contains__(self, other):
        return self.__generate_filter(operator.contains, other)

    def __eq__(self, other):
        return self.__generate_filter(operator.eq, other)

    def in_(self, other):
        return self.__generate_filter(operator.contains, other)

    def is_(self, other):
        return self.__generate_filter(operator.is_, other)

    def __and__(self, other: 'FilterObject'):
        self.related.append((operator.and_, other))
        return self

    def __or__(self, other: 'FilterObject'):
        self.related.append((operator.or_, other))
        return self


class FilterObject(OperatorsMixin):
    def __init__(self, object_name: str):
        self.name: str = object_name
        self.operator = None
        self.value = None
        self.related: List[Tuple[operator, 'FilterObject']] = []

    def get_nested_objects(self, input_object: BaseModel):
        parts = self.name.split(".")
        for part in parts:
            input_object = getattr(input_object, part, None)
            if input_object is None:
                return None

        return input_object

    def condition_request(self, input_object: BaseModel):
        object_get = (
            getattr(input_object, self.name, None)
            if "." not in self.name
            else self.get_nested_objects(input_object)
        )
        operator_result: bool = True

        if object_get is None:
            raise ValueError(f'Filter \'{self.name}\' does not exist in passed object')

        if self.operator is not None:
            operator_result = self.operator(self.value, object_get)

        if not self.related:
            return operator_result

        for operator_, filter_ in self.related:
            search_result: bool = filter_.condition_request(input_object)
            operator_result: bool = operator_(operator_result, search_result)

        return operator_result

    def __hash__(self):
        return hash(self.name)

    def __getattr__(self, item):
        self.name += f".{item}"
        return self

    def __call__(self, prefix: str):
        self.prefix = prefix
        return self


class FilterHandler:
    def __getattr__(self, item: str):
        filter_ = FilterObject(item)
        return filter_


F = FilterHandler()
