import asyncio
from http import HTTPStatus
from app import Application


async def main():
    appication = Application()
    responce = await appication.handle_request(
        {}, "POST", "http://docs.python.org:80/3/library/urllib.parse.html?", {}
    )
    # print(list(HTTPStatus))
    d = {s.value: s.phrase for s in HTTPStatus}
    print(d)


if __name__ == "__main__":
    asyncio.run(main())
