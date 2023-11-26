import asyncio

from http_request import parse_http_request, create_http_response


class HttpServer:

    def __init__(self, host: str, port: int, app: ...) -> None:
        self.host = host
        self.port = port
        self.app = app

    async def handle_client(self, reader, writer):
        address = writer.get_extra_info('peername')
        print(f"Accepted connection from {address}")

        request_data = await reader.read(4096)
        print(f"\tReceived data: {request_data.decode('utf-8')}")
        try:
            parsed_request = parse_http_request(request_data)
            print(f"{parsed_request=}")
            response, status_code = await self.app.handle_request(**parsed_request)
        except Exception as ex:
            print(f"Can't parse HTTP request, reason: {ex}")
            response, status_code = {"error": "Can't parse HTTP request"}, 404

        response_data = create_http_response(response, status_code=status_code)
        writer.write(response_data)
        await writer.drain()
        print(f"Sent data: {response_data.decode('utf-8')}")

        print(f"Closing connection from {address}")
        writer.close()

    async def run_server(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        print(f"Server listening on port {self.port}")

        async with server:
            await server.serve_forever()

    async def run(self):
        await self.run_server()

    def run_forever(self):
        asyncio.run(self.run())
