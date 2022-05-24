from datetime import datetime


def timestamp_as_string():
    return datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
