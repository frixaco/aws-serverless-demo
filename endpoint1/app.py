import json

import utilities
from database import connect_to_db


def main(event):
    utilities.init_db()
    connect_to_db()

    payload = event["data"]["message"]

    message = json.dumps(payload)

    return {"message": message, "success": True}


def lambda_handler(event, context):
    print("============ EVENT: ", event)
    response = main(event)
    print("============ RESPONSE: ", response)

    return response
