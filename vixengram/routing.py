import inspect
import traceback
from functools import wraps
from typing import Callable, Coroutine, Dict, List, Any
from pydantic import BaseModel

from vixengram.filters.base import FilterObject


class Router:
    def __init__(self, title: str | None = None):
        """
        Title need for VixenAPI generator
        """
        self.title = title or inspect.getouterframes(inspect.currentframe())[1].filename
        self.included_routers: List[Router] = []
        self.paths: Dict[Callable[..., Any], FilterObject] = {}
        self.__paths_with_included: Dict[Callable[..., Any], FilterObject] = {}
        self.command_args: List | None = None
        # todo: add Middleware class
        # self.__middlewares: List = []

    # async def __call_middlewares(self, handler: Optional[Callable] = None, input_object: Optional[BaseModel] = None):
    #     for middleware in self.__middlewares:
    #         await middleware()
    #
    #     for router in self.__included_routers:
    #         if handler in router:
    #             await router.__call_middlewares(input_object=input_object)

    async def set_parameters(self, handler, input_object) -> Dict[str, str | None]:
        need_parameters = inspect.signature(handler).parameters
        parameters: Dict[str, str | None] = {}
        for need_param, annotation in need_parameters.items():
            if annotation.annotation:
                parameters[need_param] = annotation.annotation(input_object)

        return parameters

    async def call_handler(self, input_object: BaseModel):
        for handler, filter_ in self.__paths_with_included.items():
            if filter_ is not None and not filter_.condition_request(input_object):
                continue

            parameters = await self.set_parameters(handler, input_object)
            # await self.__call_middlewares(handler=handler, input_object=input_object)
            await handler(**parameters)

    def add_route(
        self, filter_: FilterObject, handler: Callable[..., Coroutine]
    ) -> None:
        self.__paths_with_included[handler] = filter_
        self.paths[handler] = filter_

    def message(self, filter_: FilterObject | None = None):
        def decorator(fn):
            @wraps(fn)
            async def wrapper(*args, **kwargs) -> Coroutine:
                try:
                    result = await fn(*args, **kwargs)
                    # todo: add action logger
                    return result
                except Exception:
                    # todo: add tb logger
                    traceback.print_exc()

            self.add_route(filter_, wrapper)
            return wrapper

        return decorator

    def include_router(self, router: "Router") -> None:
        self.included_routers.append(router)
        self.__paths_with_included.update(router.__paths_with_included)

    def get_routers(self) -> List["Router"]:
        if not self.included_routers:
            return [self]

        routers = [
            router
            for routers_pack in self.included_routers
            for router in routers_pack.get_routers()
            if routers_pack is not None
        ]
        routers.append(self)
        return routers
