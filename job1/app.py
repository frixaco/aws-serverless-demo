def main(event):
    return {"message": "job 1"}


def lambda_handler(event, context):
    print("============ EVENT: ", event)
    response = main(event)
    print("============ RESPONSE: ", response)

    return response
