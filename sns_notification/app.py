import json
import os
import time

import requests
import utilities


def main(event):
    api_url = os.environ["GRAPHQL_API_URL"]
    api_key = os.environ["GRAPHQL_API_KEY"]

    subscription_query = """
        mutation Endpoint4($receiverId: String!, $payload: NotificationInput) {
            endpoint4(receiverId: $receiverId, payload: $payload) {
              receiverId
              payload {
                content
              }
            }
        }
    """

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    message_content = json.loads(event["Records"][0]["Sns"]["Message"])
    receiver_id = message_content.get("receiverId", None)
    payload = message_content.get("payload", None)

    print("receiverId", receiver_id)
    print("payload", payload)

    if not receiver_id or not payload:
        raise Exception("Invalid receiverId or payload")

    subscription_variables = {
        "receiverId": receiver_id,
        "payload": payload,
    }

    subscription_payload = {
        "query": subscription_query,
        "variables": subscription_variables,
    }

    response = requests.post(
        api_url, headers=headers, data=json.dumps(subscription_payload)
    )

    return response.json()


def lambda_handler(event, context):
    print("=============== EVENT: ", event)
    response = main(event)
    print("=============== RESPONSE: ", response)

    return response
