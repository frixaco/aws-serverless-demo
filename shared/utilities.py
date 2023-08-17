import os
import subprocess

from database import connect_to_db


def check_ffmpeg_opt():
    ffmpeg_binary = "/opt/python/ffmpeg"

    if not os.path.exists(ffmpeg_binary):
        print("ffmpeg binary not found")
        return False

    print("ffmpeg binary found")

    result = subprocess.run(
        [ffmpeg_binary, "--version"],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    print(result.stderr)

    return True


def check_ffmpeg():
    ffmpeg_binary = "ffmpeg"

    if not os.path.exists(ffmpeg_binary):
        print("ffmpeg binary not found")
        return False

    print("ffmpeg binary found")

    result = subprocess.run(
        [ffmpeg_binary, "--version"],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    print(result.stderr)

    return True


def init_db():
    return connect_to_db()
