from typing import Dict
from urllib.parse import urlparse


class Application:
    def __init__(self):
        self.routes: Dict[str, callable] = {}
        pass

    def register_route(self, url, handler, method):
        self.routes[url] = method
        pass

    def run_server(self):
        pass

    async def handle_request(self, method:str, path:str, params:dict) -> None :
        if (method, path) not in self.routes:
            return 'HTTP/2 404 Not Found'
        
        handler = self.routes[(method, path)]

        
        response = handler(**params)
        

