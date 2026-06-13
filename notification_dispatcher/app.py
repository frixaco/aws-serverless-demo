import json
import os

import requests


PUBLISH_NOTIFICATION_MUTATION = """
mutation PublishNotification($receiverId: String!, $payload: NotificationInput!) {
  publishNotification(receiverId: $receiverId, payload: $payload) {
    receiverId
    payload {
      activityId
      message
    }
  }
}
"""


def main(event):
    record = event["Records"][0]
    message = json.loads(record["Sns"]["Message"])

    receiver_id = message["receiverId"]
    payload = message["payload"]

    response = requests.post(
        os.environ["GRAPHQL_API_URL"],
        headers={
            "Content-Type": "application/json",
            "x-api-key": os.environ["GRAPHQL_API_KEY"],
        },
        json={
            "query": PUBLISH_NOTIFICATION_MUTATION,
            "variables": {
                "receiverId": receiver_id,
                "payload": payload,
            },
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def lambda_handler(event, context):
    print("event:", event)
    response = main(event)
    print("response:", response)
    return response
