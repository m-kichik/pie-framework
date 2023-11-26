from http import HTTPStatus
from src.app import Dispatcher
from src.server import Server
import src.orm as orm


class User(orm.Model):
    id = orm.IntegerField()
    name = orm.TextField()
    age = orm.IntegerField()


def get_hello_world(**query_params):
    return {
        "msg": "response from hello world",
        "query_params": query_params,
    }, 200


def post_hello_world(json_data, **query_params):
    return {
        "msg": "response from hello world",
        "json_data": json_data,
        "query_params": query_params,
    }, 200


if __name__ == "__main__":
    orm.Model.connect("./my_db.sqlite3")
    User.create_entity()
    def post_uesers(users_json, **params):
        for i, user in enumerate(users_json):
            user = User(i+1, user['name'], user['age'])
            user.save()
        return {"resp": "ok"}, HTTPStatus.OK
    
    def get_users(**params):
        response = []
        for user in User.get():
            response.append({
                "id": user[0],
                "name": user[1],
                "age": user[2],
            })
        return response, HTTPStatus.OK
    
    app = Dispatcher()
    app.register_route("GET", "/hello/world", get_hello_world)
    app.register_route("POST", "/hello/world", post_hello_world)
    app.register_route("GET", "/users", get_users)
    app.register_route("POST", "/users", post_uesers)

    server = Server("localhost", 8080, app)
    server.run()
