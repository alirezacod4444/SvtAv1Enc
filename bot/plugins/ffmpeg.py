import asyncio
import math
import re
import subprocess
import time
from random import randint

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from html_telegraph_poster import TelegraphPoster

from bot import LOGS, bot


class ffmpeg(object):

    async def resolution(filepath):
        metadata = extractMetadata(createParser(filepath))
        if metadata.has("width") and metadata.has("height"):
            return metadata.get("width"), metadata.get("height")
        else:
            return 1280, 720

    async def duration(filepath):
        try:
            process = subprocess.Popen(
                ["ffmpeg", "-hide_banner", "-i", filepath],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            stdout, stderr = process.communicate()
            output = stdout.decode().strip()
            duration = re.search(
                "Duration:\\s*(\\d*):(\\d*):(\\d+\\.?\\d*)[\\s\\w*$]", output)
            bitrates = re.search("bitrate:\\s*(\\d+)[\\s\\w*$]", output)
            if duration is not None:
                hours = int(duration.group(1))
                minutes = int(duration.group(2))
                seconds = math.floor(float(duration.group(3)))
                total_seconds = (hours * 60 * 60) + (minutes * 60) + seconds
                int(total_seconds)
            else:
                total_seconds = 00
            return total_seconds
        except Exception as e:
            LOGS.info(e)


class functions(object):

    async def sample(filepath, output):
        try:
            time.time()
            output_file = output
            duration = await ffmpeg.duration(filepath=filepath)
            sample_duration = 30
            best_duration = duration - sample_duration
            ss = randint(1, int(best_duration))
            file_gen_cmd = f'ffmpeg -loglevel error -ss {str(ss)} -i "{filepath}" -c copy -map 0 -t {str(sample_duration)} "{output_file}" -y'
            process = await asyncio.create_subprocess_shell(
                file_gen_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            LOGS.info(stderr)
            return output_file
        except Exception:
            return None

    async def screenshot(filepath):
        time_latest = time.time()
        screenshot = f"{time_latest}.jpg"
        duration = await ffmpeg.duration(filepath=filepath)
        ss = randint(2, duration)
        cmd = f'ffmpeg -ss {str(ss)} -i "{filepath}" -vframes 1 "{screenshot}" -y'
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return screenshot

    def __init__(self):
        self.base__url = "t.me"

    async def mediainfo(filepath):
        try:
            process = subprocess.Popen(
                ["mediainfo", filepath, "--Output=HTML"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            stdout, stderr = process.communicate()
            out = stdout.decode()
            abc = await bot.get_me()
            name = abc.first_name
            username = abc.username
            client = TelegraphPoster(use_api=True)
            client.create_api_token("Mediainfo")
            page = client.post(
                title="Mediainfo",
                author=name,
                author_url=f"https://t.me/{username}",
                text=out,
            )
            return page["url"]
        except Exception as e:
            LOGS.info(e)
            return "404"
