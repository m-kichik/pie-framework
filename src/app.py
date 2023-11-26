import inspect
from typing import Dict, Callable, Literal, Awaitable


class Dispatcher:

    def __init__(self):
        self.routes: Dict[tuple[str, str], Callable | Awaitable] = {}

    def register_route(self, method: Literal['GET', 'POST'], path: str, handler: Callable | Awaitable) -> None:
        if (method, path) in self.routes:
            raise ValueError(f"Handler {method=} {path=} already registered")
        self.routes[(method, path)] = handler

    async def handle_request(self, method: str, path: str, data: dict) -> tuple[dict, int]:
        if (method, path) not in self.routes:
            return {"error": "Not found"}, 404
        handler = self.routes[(method, path)]
        if inspect.isawaitable(handler):
            return await handler(**data)
        return handler(**data)
