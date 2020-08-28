import datetime
import logging
import os

logger = logging.getLogger(__name__)


def remove_file(filepath, stub=True):
    if stub:
        print(f"Removing: {filepath}")
        logger.debug(f"Fake remove file: {filepath}")
    else:
        os.remove(filepath)
        logger.debug(f"Remove file: {filepath}")


def set_bit(v, index, x):
    mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
    v &= ~mask  # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask  # If x was True, set the bit indicated by the mask.
    return v  # Return the result, we're done.


def get_bit(v, index):
    return (v & (1 << index)) >> index


def get_wav_last_modify_date_time(path_to_wav_file):
    return datetime.datetime.utcfromtimestamp(os.path.getmtime(path_to_wav_file))


def format_phone_call_to_log(date_time, stage_number, answer, phone_number, duration, transcription):
    return f"{date_time.date()} {date_time.time()}, <{int(date_time.timestamp())}>, " \
           f"stage: {stage_number}, answer: {answer}, phone_number: +{phone_number}, " \
           f"duration: {duration}, transcription: \"{transcription}\""
