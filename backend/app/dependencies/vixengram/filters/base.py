from typing import List, Tuple, Any, Callable, Self

from pydantic import BaseModel
import operator

T = List[Tuple[Callable[..., Any], "FilterObject"]]


class OperatorsMixin:
    """
    Миксин для подмешивания операторов в FilterObject
    """

    related: T
    operator: Callable[..., Any] | None

    def __generate_filter(self, operator_object: Callable[..., Any], other: Any):
        self.operator = operator_object
        self.value = other
        return self

    def __contains__(self, other: Any) -> Self:
        return self.__generate_filter(operator.contains, other)

    def __eq__(self, other: Any) -> Self:  # type: ignore
        return self.__generate_filter(operator.eq, other)

    def in_(self, other: Any) -> Self:
        return self.__generate_filter(operator.contains, other)

    def is_(self, other: Any) -> Self:
        return self.__generate_filter(operator.is_, other)

    def __and__(self, other: "FilterObject") -> Self:
        self.related.append((operator.and_, other))
        return self

    def __or__(self, other: "FilterObject") -> Self:
        self.related.append((operator.or_, other))
        return self


class FilterObject(OperatorsMixin):
    def __init__(self, object_name: str):
        """
        name: Путь до требуемого параметра в объекте Message.
        operator: Оператор, который будет использоваться для сравнения.
        value: Параметр, который требуется найти.
        related: Связанные с этим фильтры, которые образуют из себя большое выражение.
        need_args: Булево значение, которое определяет, требуется ли сохранять текст, после найденного аргумента (или минуя его, он заменяется на '').
        """
        self.name: str = object_name
        self.operator: Callable[..., Any] | None = None
        self.value: Any = None
        self.related: T = []
        self.need_args: bool = False

    def get_nested_objects(self, input_object: BaseModel):
        parts: List[str] = self.name.split(".")
        return_object: Any = None
        for part in parts:
            return_object = getattr(input_object, part, None)
            if return_object is None:
                return None

        return return_object

    def condition_request(self, input_object: BaseModel):
        object_get: str | None = (
            getattr(input_object, self.name, None)
            if "." not in self.name
            else self.get_nested_objects(input_object)
        )
        operator_result: bool = True

        if object_get is None:
            raise ValueError(f"Filter '{self.name}' does not exist in passed object")

        if self.operator is not None:
            operator_result = self.operator(self.value, object_get)

        if self.need_args:
            if isinstance(object_get, str):
                args = object_get.replace(f"{self.value}", "")
                input_object.__dict__.update(
                    {"_command_args": args.strip() if args else None}
                )

        if not self.related:
            return operator_result

        for operator_, filter_ in self.related:
            search_result: bool = filter_.condition_request(input_object)
            operator_result = operator_(operator_result, search_result)

        return operator_result

    def __hash__(self):
        return hash(self.name)

    def __getattr__(self, item: str):
        self.name += f".{item}"
        return self

    def __call__(self, prefix: str):
        self.prefix = prefix
        return self


class FilterHandler:
    """
    Родитель для FilterObject`а, для более удобного с ним взаимодействия
    """

    def __getattr__(self, item: str):
        filter_ = FilterObject(item)
        return filter_


F = FilterHandler()
