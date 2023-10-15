import os
import random
import re
import time

from pyrogram.types import InputMediaPhoto

from bot import LOGS, Config, bot
from bot.database import (adduser, getffmpeg, setffmpeg, setmode, uploadtype,
                          uploadtype1)

from .devtools import progress_for_pyrogram
from .ffmpeg import ffmpeg, functions


async def changeffmpeg(bot, message):
    try:
        await adduser(message)
        changeffmpeg = message.text.split(" ", maxsplit=1)[1]
        await setffmpeg(message, changeffmpeg)
        print(changeffmpeg)
        await message.reply_text("🗜 **Changed FFmpeg Code.**", quote=True)
    except Exception as e:
        await message.reply_text(f"❗️**Error:** `{e}`", quote=True)


async def changemode(bot, message):
    try:
        newmode = message.text.split(" ", maxsplit=1)[1]
        if "video" == newmode:
            await setmode(message, newmode)
            await bot.send_message(
                text="🎞️ **Changed Upload Mode.**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
        elif "document" == newmode:
            await setmode(message, newmode)
            await bot.send_message(
                text="📄 **Changed Upload Mode.**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
        else:
            await bot.send_message(
                text="❌ **Unknown Upload Type.**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
    except Exception as e:
        await bot.send_message(
            text=f"❗️**Error:** `{e}`",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id,
        )


async def download_dir(bot, message):
    d_start = time.time()
    if message.reply_to_message:
        reply = await bot.send_message(
            text=f"📥 **Downloading Video:**",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id,
        )
        video = await bot.download_media(
            message=message.reply_to_message,
            file_name=Config.TEMP,
            progress=progress_for_pyrogram,
            progress_args=(bot, "📥 **Downloading Video:**", reply, d_start),
        )
        await reply.edit(f"📂 **Directory Is:** `{video}`")
    else:
        await bot.send_message(
            text=f"⚠️ **Reply To A File To Download It.**",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id,
        )


emoji = (
    "🤓",
    "😎",
    "🤠",
    "🌚",
    "🛰️",
    "❤️",
    "📡",
    "🥺",
    "🌝",
    "☺️",
    "😊",
    "😑",
    "📌",
    "🥸",
    "😵‍💫",
    "🪩",
    "✅",
)

emoji2 = (
    "❌",
    "❎",
    "✖️",
    "☠️",
    "💀",
    "🧟",
    "💔",
    "⚰️",
    "⛔",
    "🫠",
)

quip = (
    "Awake And Ready To Serve You, Young Master!",
    "Up!",
    "A Coconut.",
    "The Fastest Bot Alive.",
    "Ready To Encode From Dusk Till Dawn.",
    "Ready And Awaiting Orders, Sir! Yes Sir!",
    "Feeling Lucky+",
    "(Technically) A Noble Bot.",
    "The... Core!",
    "Stunned, Yet Not Surprised, By Your Kind Gesture.",
    "The Highest Bot.",
    "The Archduke’s Daughter, Maiodore In Disguise.",
    "Ready!",
)


def enmoji():
    return random.choice(emoji)


def enmoji2():
    return random.choice(emoji2)


def enquip():
    return random.choice(quip)


async def get_ffmpeg(bot, message):
    ffmpegcodee = await getffmpeg(message)
    print(ffmpegcodee)
    await bot.send_message(
        text=f"🗜 **Current FFmpeg Code:**\n\n`{ffmpegcodee}`",
        chat_id=message.from_user.id,
        reply_to_message_id=message.id,
    )


async def get_type(bot, message):
    upload_type = await uploadtype(message)
    await bot.send_message(
        text=f"🔺 **Upload Mode:** `{upload_type}`",
        chat_id=message.from_user.id,
        reply_to_message_id=message.id,
    )


async def sample(bot, message):
    if message.reply_to_message:
        d_start = time.time()
        reply = await bot.send_message(
            text="📥 **Downloading Video:**",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id,
        )
        video = await bot.download_media(
            message=message.reply_to_message,
            file_name=Config.TEMP,
            progress=progress_for_pyrogram,
            progress_args=(bot, "📥 **Downloading Video:**", reply, d_start),
        )
        path, filename = os.path.split(video)
        output_filename = filename + "_sample.mkv"
        await reply.edit("🚀 **Generating Sample...**")
        sample = await functions.sample(filepath=video, output=output_filename)
        caption = filename + " SAMPLE"
        await upload_handle(bot, message, sample, filename, caption, reply)
        os.remove(video)
        os.remove(sample)
        await reply.delete(True)
    else:
        await bot.send_message(
            text=f"⚠️ **Reply To A File To Download It.**",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id,
        )


async def upload_dir(client, message):
    u_start = time.time()
    if message.reply_to_message:
        message = message.reply_to_message
    cmd1 = message.text.split(" ", maxsplit=1)[1]
    replyid = message.id
    if message.from_user.id in Config.OWNER:
        if os.path.exists(cmd1):
            xhamster = await bot.send_message(
                text=f"📤 **Uploading File:**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
            await client.send_document(
                chat_id=message.chat.id,
                document=cmd1,
                caption=cmd1,
                reply_to_message_id=replyid,
                progress=progress_for_pyrogram,
                progress_args=(client, "📤 **Uploading File:**", xhamster,
                               u_start),
            )
            await xhamster.delete()
        else:
            await bot.send_message(
                text=f"❌ **File Directory Not Found:**\n`{cmd1}`",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
    elif Config.TEMP in cmd1:
        if os.path.exists(cmd1):
            xhamster = await bot.send_message(
                text=f"📤 **Uploading File:**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
            await client.send_document(
                chat_id=message.chat.id,
                document=cmd1,
                caption=cmd1,
                reply_to_message_id=replyid,
                progress=progress_for_pyrogram,
                progress_args=(client, "📤 **Uploading File:**", xhamster,
                               u_start),
            )
            await xhamster.delete()
        else:
            await bot.send_message(
                text=f"❌ **File Directory Not Found:**\n`{cmd1}`",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
    else:
        await bot.send_message(
            text=
            f"🛑 **Access Denied.** You're Not Authorized To Access This Directory.",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id,
        )


async def vshots(bot, message):
    if message.reply_to_message:
        cmd1 = int(message.text.split(" ", maxsplit=1)[1])
        if cmd1 > 10:
            await message.reply_text(
                "⚠️ **Please provide a number between 1 and 10.**")
        else:
            d_start = time.time()
            reply = await bot.send_message(
                text="📥 **Downloading Video:**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
            )
            video = await bot.download_media(
                message=message.reply_to_message,
                file_name=Config.TEMP,
                progress=progress_for_pyrogram,
                progress_args=(bot, "📥 **Downloading Video:**", reply, d_start),
            )
            photos = []
            for x in range(1, cmd1 + 1):
                ss = await functions.screenshot(filepath=video)
                photos.append(str(ss))
                await reply.edit(f"🚀 **Uploading Photo {x}/{cmd1}...**")
            await reply.edit(f"🚀 **Starting To Upload {cmd1} Photos...**")
            await bot.send_media_group(
                chat_id=message.from_user.id,
                reply_to_message_id=message.id,
                media=[InputMediaPhoto(media=photo) for photo in photos],
            )
            for photo in photos:
                os.remove(photo)
            await reply.delete()
            os.remove(video)
    else:
        await message.reply_text("⚠️ **Reply To A File To Download It.**",
                                 quote=True)


async def upload_handle(bot, message, filepath, filename, caption, reply):
    try:
        if os.path.exists(filepath) == False:
            return bot.send_message(
                chat_id=from_user_id,
                text="❌ **File Not Found Unable To Upload.**")
        filename = filename.replace("#", "")
        mode = await uploadtype(message)
        if mode != "video":
            u_start = time.time()
            thumb = await functions.screenshot(filepath)
            width, height = await ffmpeg.resolution(filepath)
            duration2 = await ffmpeg.duration(filepath)
            s = await bot.send_video(
                video=filepath,
                chat_id=message.from_user.id,
                supports_streaming=True,
                file_name=filename,
                thumb=thumb,
                duration=duration2,
                width=width,
                height=height,
                caption=caption,
                reply_to_message_id=message.id,
                progress=progress_for_pyrogram,
                progress_args=(bot, "📤 **Uploading Video:**", reply, u_start),
            )
            os.remove(thumb)
        else:
            u_start = time.time()
            thumb = await functions.screenshot(filepath)
            width, height = await ffmpeg.resolution(filepath)
            duration2 = await ffmpeg.duration(filepath)
            s = await bot.send_video(
                video=filepath,
                chat_id=message.from_user.id,
                supports_streaming=True,
                file_name=filename,
                thumb=thumb,
                duration=duration2,
                width=width,
                height=height,
                caption=caption,
                reply_to_message_id=message.id,
                progress=progress_for_pyrogram,
                progress_args=(bot, "📤 **Uploading Video:**", reply, u_start),
            )
            os.remove(thumb)
    except Exception as e:
        LOGS.info(e)


async def upload_handle1(bot, from_user_id, filepath, filename, caption, reply,
                         reply_to_message):
    try:
        if os.path.exists(filepath) == False:
            return bot.send_message(
                chat_id=from_user_id,
                text="❌ **File Not Found Unable To Upload.**")
        filename = filename.replace("#", "")
        if not re.search(r"_S\d+", filename):
            caption = caption.replace("#", "").replace("_", " ")
        mode = await uploadtype1(from_user_id)
        if mode == "document":
            u_start = time.time()
            thumb = await functions.screenshot(filepath)
            s = await bot.send_document(
                document=filepath,
                chat_id=from_user_id,
                force_document=True,
                file_name=filename,
                thumb=thumb,
                reply_to_message_id=reply_to_message,
                progress=progress_for_pyrogram,
                progress_args=(bot, "📤 **Uploading Video:**", reply, u_start),
            )
            os.remove(thumb)
            await s.forward(Config.LOG_CHANNEL)
        elif mode == "video":
            u_start = time.time()
            thumb = await functions.screenshot(filepath)
            width, height = await ffmpeg.resolution(filepath)
            duration2 = await ffmpeg.duration(filepath)
            caption_text = (
                f"🔻<b>{caption.replace(' [@XtasyFlicks]', '').replace('¿', '')}</b>"
            )
            s = await bot.send_video(
                video=filepath,
                chat_id=from_user_id,
                supports_streaming=True,
                file_name=filename,
                thumb=thumb,
                duration=duration2,
                width=width,
                height=height,
                caption=caption_text,
                reply_to_message_id=reply_to_message,
                progress=progress_for_pyrogram,
                progress_args=(bot, "📤 **Uploading Video:**", reply, u_start),
            )
            os.remove(thumb)
            await s.forward(Config.LOG_CHANNEL)
    except Exception as e:
        LOGS.info(e)
