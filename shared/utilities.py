import json
import os
import subprocess
from typing import TypedDict

import boto3
from database import connect_to_db


class NotificationPayload(TypedDict):
    content: str


def notify_subscribers(payload: NotificationPayload, topic_arn: str, receiver_id: str):
    print("============ START NOTIFY SUBSCRIBERS ============")
    print("sns topic arn: ", topic_arn)
    print("message: ", {"receiverId": receiver_id, "payload": payload})

    sns = boto3.client("sns")
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(
            {"default": json.dumps({"receiverId": receiver_id, "payload": payload})}
        ),
        MessageStructure="json",
    )

    print("sns response: ", response)
    print("============ FINISHED NOTIFYING SUBSCRIBERS ============")

    return response


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
