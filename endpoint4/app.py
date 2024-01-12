def main(event):
    receiver_id = event.get("receiverId", None)
    payload = event.get("payload", None)

    return {"receiverId": receiver_id, "payload": payload}


def lambda_handler(event, context):
    print("============ EVENT: ", event)
    response = main(event)
    print("============ RESPONSE: ", response)

    return response
