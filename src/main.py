from app import Dispatcher
from server import HttpServer


# example of usage:
def get_user(name: str) -> dict:
    return {"username": "Name"}


app = Dispatcher()
app.register_route(method="GET", path="/api/users/", handler=get_user)
server = HttpServer(host="127.0.0.1", port=8000, app=app)
server.run_forever()
