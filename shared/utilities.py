import json
from typing import Any, TypedDict

import boto3


class NotificationPayload(TypedDict):
    activityId: str
    message: str


def demo_source_name(source: str) -> str:
    return f"aws-serverless-demo:{source}"


def identity_user_id(identity: dict[str, Any]) -> str:
    return (
        identity.get("sub")
        or identity.get("username")
        or identity.get("apiKey")
        or "anonymous-demo-user"
    )


def notify_subscribers(
    *,
    payload: NotificationPayload,
    topic_arn: str,
    receiver_id: str,
):
    message = {"receiverId": receiver_id, "payload": payload}
    sns = boto3.client("sns")
    return sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps({"default": json.dumps(message)}),
        MessageStructure="json",
    )
