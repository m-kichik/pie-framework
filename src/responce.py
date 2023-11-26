
class Response:
    def __init__(self, status: int, reason: str, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
