from http import HTTPStatus
from src.app import Dispatcher
from src.server import HttpServer
import src.orm as orm


class User(orm.Model):
    id = orm.IntegerField()
    name = orm.TextField()
    age = orm.IntegerField()


def root() -> tuple[dict, HTTPStatus]:
    return {
        "message": "Welcome to the Pie Framework!",
        "description": "Pie is a lightweight and flexible Python web framework for building web applications.",
        "version": "1.0.0",
    }, HTTPStatus.OK


def get_hello_world(**query_params) -> tuple[dict, HTTPStatus]:
    return {
        "msg": "response from hello world",
        "query_params": query_params,
    }, HTTPStatus.OK


def post_hello_world(**kwargs) -> tuple[dict, HTTPStatus]:
    return {
        "msg": "response from hello world",
        "kwargs": kwargs,
    }, HTTPStatus.OK


def create_user(users: list[dict]) -> tuple[dict, HTTPStatus]:
    for i, user in enumerate(users):
        user = User(i + 1, user['name'], user['age'])
        user.save()
    return {"resp": "ok"}, HTTPStatus.OK


def get_users(**params) -> tuple[list[dict], HTTPStatus]:
    response = []
    for user in User.get():
        response.append({
            "id": user[0],
            "name": user[1],
            "age": user[2],
        })
    return response, HTTPStatus.OK


if __name__ == "__main__":
    orm.Model.connect("./my_db.sqlite3")
    User.create_entity()

    app = Dispatcher()
    app.register_route("GET", "/", root)
    app.register_route("GET", "/hello_world", get_hello_world)
    app.register_route("POST", "/hello_world", post_hello_world)
    app.register_route("GET", "/users", get_users)
    app.register_route("POST", "/users", create_user)

    server = HttpServer("localhost", 8080, app)
    server.run_forever()
