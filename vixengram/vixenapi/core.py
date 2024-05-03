import inspect
from enum import Enum
from types import LambdaType
from typing import List, Optional, Dict, Any, Callable

from vixengram.filters.base import FilterObject
from vixengram.routing import Router

T = Optional[List[Router]]


class Operators(Enum):
    eq = "=="
    contains = "in"


class VixenAPIGenerator:
    def __init__(self, title: str, version: str, routers: T):
        self.title: str = title
        self.version: str = version
        self.routers: T = routers
        self.json: Dict[str, Dict[str, Any] | List[Dict[str, Any]] | str] = {}

    def generate_json(self) -> dict:
        self.json.update(
            {
                "title": self.title,
                "version": self.version,
                "routes": self.get_routers(),
            }
        )
        return self.json

    def _get_operator_type(self, operator_: Callable[..., Any] | None) -> str:
        if operator_ is None:
            return "N/A"

        return (
            "Custom lambda operator"
            if isinstance(operator_, LambdaType)
            else getattr(Operators, operator_.__name__).value
        )

    def _generate_filter_dict(self, filter_: FilterObject) -> Dict[str, Any]:
        return {
            "name": filter_.name if filter_.name != "data" else "CallbackData",
            "operator": self._get_operator_type(filter_.operator),
            "value": [filter_.value] if not isinstance(filter_.value, list) else filter_.value,
            "command_param": filter_.need_args,
        }

    def _parse_annotation(self, annotation: Any) -> str | None:
        parts = str(annotation).split(".")
        if parts == 0:
            return None

        remove_section: str = parts[-1].replace("'>", "")
        return remove_section

    def _extract_arguments(self, function: Callable[..., Any]) -> Dict[str, str | None]:
        parameters = inspect.signature(function).parameters.values()
        return {
            parameter.name: self._parse_annotation(parameter.annotation)
            for parameter in parameters
        }

    def _get_routes_from_router(self, router: Router):
        routes: Dict[str, Dict[str, Any]] = {}
        router_title = router.title or router.__repr__()
        for function, filter_ in router.paths.items():
            fn_name = function.__name__

            if fn_name in routes:
                routes[fn_name]["filters"].append(self._generate_filter_dict(filter_))
                continue

            routes[fn_name] = {
                "name": fn_name,
                "router": router_title,
                "filters": [self._generate_filter_dict(filter_)],
                "function_arguments": self._extract_arguments(function),
            }

        return routes

    def get_routers(self) -> List[Dict[str, Any]]:
        if not self.routers:
            return []

        return [
            route_data
            for router in self.routers
            for route_name, route_data in self._get_routes_from_router(router).items()
        ]
