import asyncio


class Server:
    def __init__(self):
        pass

    async def handle_client(self, reader, writer):
        address = writer.get_extra_info('peername')
        print(f"Accepted connection from {address}")

        request_data = await reader.read(4096)
        print(f"Received data: {request_data.decode('utf-8')}")

        # Replace this with your own response logic
        response_data = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!\r\n"

        writer.write(response_data)
        await writer.drain()
        print(f"Sent data: {response_data.decode('utf-8')}")

        print(f"Closing connection from {address}")
        writer.close()

    async def run_server(self):
        server = await asyncio.start_server(
            self.handle_client, '127.0.0.1', 8080
        )
        print("Server listening on port 8080")

        async with server:
            await server.serve_forever()

    async def run(self):
        await self.run_server()
