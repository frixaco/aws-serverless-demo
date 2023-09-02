import utilities
import uuid6
from database import connect_to_db, use_ffmpeg


def use_external_library():
    print(uuid6.uuid6())


def main(event):
    utilities.check_ffmpeg()
    utilities.check_ffmpeg_opt()
    utilities.init_db()
    connect_to_db()
    use_ffmpeg()

    use_external_library()

    message = event["data"]["message"]

    return {"message": message, "success": True}


def lambda_handler(event, context):
    print("============ EVENT: ", event)
    response = main(event)

    return response
