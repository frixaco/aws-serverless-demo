import utilities


def use_ffmpeg():
    utilities.check_ffmpeg()
    utilities.check_ffmpeg_opt()


def connect_to_db():
    print("connected to db")

    return True
