import json

from bot import LOGS, collection, data, list_handler, queue

ffmpeg = "-c:v libsvtav1 -pix_fmt yuv420p10le -svtav1-params tune=0 -g 240 -map 0:v:0 -c:a libopus -ac 2 -map 0:a -map 0:s?"


async def adduser(message):
    if collection.find_one({"_id": int(message.from_user.id)}):
        LOGS.info("YES")
    else:
        post = {
            "_id": int(message.from_user.id),
            "ffmpeg": ffmpeg,
            "mode": "video"
        }
        collection.insert_one(post)


async def napana():
    queries = queue.find({})
    for query in queries:
        que = str(query["message"])
        b = json.loads(que)
        if not query["_id"] in list_handler:
            list_handler.append(query["_id"])
        if b not in data:
            data.append(b)


async def getffmpeg(message):
    dic = collection.find_one({"_id": int(message.from_user.id)})
    ffmpeg = dic["ffmpeg"]
    return ffmpeg


async def getffmpeg1(message):
    dic = collection.find_one({"_id": int(message)})
    ffmpeg = dic["ffmpeg"]
    return ffmpeg


async def setffmpeg(message, ffmpeg1):
    collection.update_one({"_id": int(message.from_user.id)},
                          {"$set": {
                              "ffmpeg": ffmpeg1
                          }})


async def setmode(message, mode):
    collection.update_one({"_id": int(message.from_user.id)},
                          {"$set": {
                              "mode": mode
                          }})


async def uploadtype(message):
    dic = collection.find_one({"_id": int(message.from_user.id)})
    mode = dic["mode"]
    return mode


async def uploadtype1(message):
    dic = collection.find_one({"_id": int(message)})
    mode = dic["mode"]
    return mode
