import asyncio
from proto.math_pb2 import AddRequest
import time

a = AddRequest()

a.x = 5
a.y = 9

print(AddRequest.SerializeToString(a))


async def slow_print(name, i):
    await asyncio.sleep(i)
    print("Hello, %s" % name)


async def main():
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(slow_print('mehdi', 5))
    t2 = loop.create_task(slow_print('sadegh', 1))
    await asyncio.sleep(10)


mainLoop = asyncio.get_event_loop()
mainLoop.run_until_complete(main())
mainLoop.close()
