from src.app import Application
from src.server import Server

def get_hello_world(json_data, **query_params):
    return f'get hello world with {json_data=}, {query_params=}'

def post_hello_world(json_data, **query_params):
    return f'post hello world{json_data=}, {query_params=}'


if __name__ == "__main__":
    app = Application()
    app.register_route("GET", "/hello/world", get_hello_world)
    app.register_route("POST", "/hello/world", post_hello_world)

    server = Server("localhost", 8080, app)
    server.run()
    
