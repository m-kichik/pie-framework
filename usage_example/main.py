from src.app import Application
from src.server import Server

def get_hello_world(json_data, **query_params):
    return f'get hello world with {json_data=}, {query_params=}'

def post_hello_world(json_data, **query_params):
    return f'post hello world{json_data=}, {query_params=}'


if __name__ == "__main__":
    app = Application()
    server = Server()

    app.register_route("/hello/world", "GET", get_hello_world)
    app.register_route("/hello/world", "POST", post_hello_world)

    server.run()
    
