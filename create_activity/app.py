import os

import utilities
import uuid6
from utilities import NotificationPayload


def main(event):
    arguments = event.get("arguments") or {}
    input_data = arguments.get("input") or {}

    activity_id = str(uuid6.uuid7())
    message = input_data["message"]
    receiver_id = input_data["receiverId"]

    payload: NotificationPayload = {
        "activityId": activity_id,
        "message": message,
    }

    topic_arn = os.environ["SNS_NOTIFICATION_TOPIC_ARN"]
    utilities.notify_subscribers(
        topic_arn=topic_arn,
        receiver_id=receiver_id,
        payload=payload,
    )

    return {
        "activityId": activity_id,
        "message": message,
        "receiverId": receiver_id,
        "notified": True,
    }


def lambda_handler(event, context):
    print("event:", event)
    response = main(event)
    print("response:", response)
    return response
