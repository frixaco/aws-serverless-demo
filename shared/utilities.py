import os
import json
import subprocess

from database import db_conn

def printer(text):
    print("Your text", text)

def check_ffmpeg_binary():
    ffmpeg_binary = "/opt/python/ffmpeg"

    if not os.path.exists(ffmpeg_binary):
        print("ffmpeg binary not found")
        return False
    
    print("ffmpeg binary found")
    return True
    

def printer(text):
    ffmpeg_path = "ffmpeg"
    cmd = f"{ffmpeg_path} --version"
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print(text, result, db_conn())
