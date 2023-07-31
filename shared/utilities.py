import os
import json

def printer(text):
    print("Your text", text)

def check_ffmpeg_binary():
    ffmpeg_binary = "/opt/python/ffmpeg"

    if not os.path.exists(ffmpeg_binary):
        print("ffmpeg binary not found")
        return False
    
    print("ffmpeg binary found")
    return True
    