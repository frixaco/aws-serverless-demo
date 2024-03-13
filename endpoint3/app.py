import utilities
from database import Session, get_users_from_db


def main(event):
    session = Session()

    utilities.init_db()
    get_users_from_db(session)

    message = event["identity"]["username"]

    return {"message": message, "success": True}


def lambda_handler(event):
    print("============ EVENT: ", event)
    response = main(event)
    print("============ RESPONSE: ", response)

    return response
