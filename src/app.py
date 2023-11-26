from typing import Dict
from urllib.parse import urlparse

from responce import Response

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
        pass

    def register_route(self, url, handler, method):
        self.routes[url] = method
        pass

    def run_server(self):
        pass

    async def handle_request(self, method:str, path:str, params:dict) -> None :
        if (method, path) not in self.routes:
            return Response(status=404, reason='Not Found')
        
        handler = self.routes[(method, path)]
        
        response = handler(**params)
        if isinstance(response, dict):
            return Response(status=response.get('status'),
                            reason=response.get('reason'),
                            headers=response.get('headers'),
                            body=response.get('body'))
        # elif isinstance(response)
