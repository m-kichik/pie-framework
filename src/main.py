from app import Dispatcher
from server import HttpServer
from http import HTTPStatus


# example of usage:

def root() -> tuple[dict, HTTPStatus]:
    return {
        "message": "Welcome to the Pie Framework!",
        "description": "Pie is a lightweight and flexible Python web framework for building web applications.",
        "version": "1.0.0",
    }, HTTPStatus.OK


def get_users() -> tuple[list, HTTPStatus]:
    return [{"name": "Test User", "age": 10}], HTTPStatus.OK


def create_user(name: str, age: int) -> tuple[dict, HTTPStatus]:
    return {"resp": "ok"}, HTTPStatus.OK


app = Dispatcher()
app.register_route(method="GET", path="/", handler=root)
app.register_route(method="GET", path="/get_users/", handler=get_users)
app.register_route(method="POST", path="/create_user/", handler=create_user)

server = HttpServer(host="127.0.0.1", port=8000, app=app)
server.run_forever()
