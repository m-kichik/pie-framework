from typing import Dict
from urllib.parse import urlparse


class Application:
    def __init__(self):
        self.routes: Dict[str, callable] = {}
        pass

    def register_route(self, url, method):
        self.routes[url] = method
        pass

    def run_server(self):
        pass

    def handle_request(self, url):
        parsed_url = urlparse(url)
        response = self.routes[url]
        return response

