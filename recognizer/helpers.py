import datetime
import os


def remove_file(filepath, stub=True):
    if stub:
        print(f"Removing: {filepath}")
    else:
        os.remove(filepath)


def get_timestamp_utc():
    return datetime.datetime.utcnow()
