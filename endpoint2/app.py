import json
import os
from time import sleep

import boto3
import requests
import utilities
import uuid6
from database import connect_to_db, use_ffmpeg
from utilities import NotificationPayload


def use_external_library():
    print(uuid6.uuid6())


def main(event):
    utilities.check_ffmpeg()
    utilities.check_ffmpeg_opt()
    utilities.init_db()
    connect_to_db()
    use_ffmpeg()

    use_external_library()

    message = event["data"]["message"]

    payload: NotificationPayload = {"content": message}

    topic_arn = os.environ["SNS_NOTIFICATION_TOPIC_ARN"]
    # ssm = boto3.client("ssm")
    # topic_arn = ssm.get_parameter(Name="topic_arn", WithDecryption=False)["Parameter"][
    #     "Value"
    # ]

    utilities.notify_subscribers(
        topic_arn=topic_arn, payload={"content": message}, receiver_id="123"
    )

    return {"message": message, "success": True}


def lambda_handler(event, context):
    print("============ EVENT: ", event)
    response = main(event)
    print("============ RESPONSE: ", response)

    return response
