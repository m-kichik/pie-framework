from app import Application

def f():
    pass

async def af():
    pass

async def main():
    # appication = Application()
    # appication.handle_request('http://docs.python.org:80/3/library/urllib.parse.html?')
    try:
        await f()
    except Exception as e:
        print('call await f', e)

    try:
        f()
    except Exception as e:
        print('call f', e)

    try:
        await af()
    except Exception as e:
        print('call await af', e)

    try:
        af()
    except Exception as e:
        print('call af', e)


await main()