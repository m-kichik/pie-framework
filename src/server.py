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
        print(f"Received data: {request_data.decode('utf-8')}")
        parsed_request = parse_http_request(request_data)

        response, status_code = await self.app.handle_request(**parsed_request)
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
        print("Server listening on port 8080")

        async with server:
            await server.serve_forever()

    async def run(self):
        await self.run_server()

    def run_forever(self):
        asyncio.run(self.run())
