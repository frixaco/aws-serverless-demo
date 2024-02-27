import utilities
from database import connect_to_db


def main(event):
    utilities.init_db()
    connect_to_db()

    message = ""
    if "data" in event:
        message = event["data"]["message"]

    return {"message": message, "success": True, "data": {"responseData": "aslkdj"}}


def lambda_handler(event, context):
    print("============ EVENT: ", event)
    response = main(event)
    print("============ RESPONSE: ", response)

    return response
