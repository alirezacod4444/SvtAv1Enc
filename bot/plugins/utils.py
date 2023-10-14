import os

from bot import LOGS, data, list_handler, queue
from bot.plugins.compress import encode


async def add_task1(m):
    try:
        await encode(m)
    except Exception as e:
        LOGS.info(e)
    await on_task_complete()


async def on_task_complete():
    del data[0]
    queue.delete_one({"_id": list_handler[0]})
    del list_handler[0]
    if len(data) > 0:
        try:
            os.system("rm encodes/*")
        except Exception:
            pass
        await add_task1(data[0])
    else:
        data.clear()
        list_handler.clear()
        queue.delete_many({})
