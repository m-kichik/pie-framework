import inspect
from typing import Dict
from urllib.parse import urlparse
from http import HTTPStatus

# from responce import Response


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
class Application:
    def __init__(self):
        self.routes: Dict[str, callable] = {}

        self.status_codes = {s.value: s.phrase for s in HTTPStatus}

    def register_route(self, url, handler, method):
        self.routes[url] = method
        pass

    def run_server(self):
        pass

    async def handle_request(
        self, json_data: dict, method: str, path: str, params: dict
    ) -> None:
        if (method, path) not in self.routes:
            return {"error": "Not found"}, 404
            # return Response(status=404, reason='Not Found')

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
        elif len(responce) != 2:
            rettypes = " ".join([str(type(item)) for item in responce])
            raise HandlerResultError(f"Handler returned ({rettypes})")
        elif not isinstance(responce[1], int):
            raise HandlerResultError(f"Handler returned non-int status code")
        elif not (isinstance(responce[0], dict) or isinstance(responce[0], list)):
            raise HandlerResultError(
                f"Handler returned {type(responce[0])} as first argument"
            )
        else:
            return responce
