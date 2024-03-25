import asyncio

async def every_thirty():
    i = 0
    while i<10:
        await asyncio.sleep(30)
        print("hi")
        i += 1
