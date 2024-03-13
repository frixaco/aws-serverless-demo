import json
import os
import subprocess
from typing import Literal, TypedDict

import boto3
from database import Session, get_users_from_db

VbratoSecrets = {
    "DATABASE_CERT": "ca-certificates.crt",
    "APPLE_INAPP_PURCHASE_KEY": "apple_subscription_key.p8",
    "APPLE_COMPUTER_ROOT_CERTIFICATE": "AppleComputerRootCertificate.cer",
    "APPLE_INC_ROOT_CERTIFICATE": "AppleIncRootCertificate.cer",
    "APPLE_ROOT_CA_G2": "AppleRootCA-G2.cer",
    "APPLE_ROOT_CA_G3": "AppleRootCA-G3.cer",
    "ANDROID_PAYWALL_SERVICE_ACCOUNT": "android_subscription_serviceaccount.json",
}

VbratoSecretKey = Literal[
    "DATABASE_CERT",
    "APPLE_INAPP_PURCHASE_KEY",
    "APPLE_COMPUTER_ROOT_CERTIFICATE",
    "APPLE_INC_ROOT_CERTIFICATE",
    "APPLE_ROOT_CA_G2",
    "APPLE_ROOT_CA_G3",
    "ANDROID_PAYWALL_SERVICE_ACCOUNT",
]

VbratoSecretReturnType = Literal["string", "bytes"]


def get_vbrato_secret(
    secret_key: VbratoSecretKey, type: VbratoSecretReturnType = "string"
):
    s3 = boto3.client("s3")

    print("Key: ", secret_key)
    print("Object URL: ", VbratoSecrets[secret_key])

    obj = s3.get_object(Bucket="frixaco-vbrato-secrets", Key=VbratoSecrets[secret_key])

    file_content = obj["Body"].read()

    match type:
        case "string":
            return file_content.decode("utf-8")
        case "bytes":
            return file_content

    return file_content


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
    session = Session()

    return get_users_from_db(session)
