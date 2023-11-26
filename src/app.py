import inspect
from http import HTTPStatus
from typing import Dict Callable, Literal, Awaitable


class HandlerResultError(Exception):
    pass


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Dispatcher:
    def __init__(self):
        self.routes: dict[tuple[str, str], Callable | Awaitable] = {}

        self.status_codes = {s.value: s.phrase for s in HTTPStatus}

    def register_route(self, method: Literal['GET', 'POST'], path: str, handler: Callable | Awaitable) -> None:
        if (method, path) in self.routes:
            raise ValueError(f"Handler {method=} {path=} already registered")
        self.routes[(method, path)] = handler

    async def handle_request(
        self, json_data: dict, method: str, path: str, params: dict
    ) -> tuple[dict, int]:
        if (method, path) not in self.routes:
            return {"error": "Not found"}, 404

        handler = self.routes[(method, path)]

        if len(json_data) == 0:
            args = []
        else:
            args = [json_data]

        if inspect.isawaitable(handler):
            responce = await handler(*args, **params)
        else:
            responce = handler(*args, **params)

        if not isinstance(responce, tuple):
            raise HandlerResultError(f"Handler returned {type(responce)}")
        if len(responce) != 2:
            rettypes = " ".join([str(type(item)) for item in responce])
            raise HandlerResultError(f"Handler returned ({rettypes})")
        if not isinstance(responce[1], int):
            raise HandlerResultError("Handler returned non-int status code")
        if not isinstance(responce[0], (dict, list)):
            raise HandlerResultError(
                f"Handler returned {type(responce[0])} as first argument"
            )

        return responce
