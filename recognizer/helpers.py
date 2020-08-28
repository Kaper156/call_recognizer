import datetime
import logging
import os

logger = logging.getLogger(__name__)


def remove_file(filepath, stub=False):
    '''
    Remove file by filepath, if flag stab is set print message
    :param filepath: path to the file
    :param stub: flag, if is set print message, instead deleting
    :return: None
    '''
    if stub:
        print(f"Removing: {filepath}")
        logger.debug(f"Fake remove file: {filepath}")
    else:
        os.remove(filepath)
        logger.debug(f"Remove file: {filepath}")


def set_bit(v, index, x):
    '''
    Set bit (x) in value (v) at index (0,1,2,...)
    :param v: value
    :param index: index at which bit will be changed
    :param x: bit value
    :return: value with changed bit
    '''
    mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
    v &= ~mask  # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask  # If x was True, set the bit indicated by the mask.
    return v  # Return the result, we're done.


def get_bit(v, index):
    '''
    Return 0 or 1 of bit at index in v(alue)
    :param v: value
    :param index: index of bit (0,1,2,...)
    :return: 0 or 1
    '''
    return (v & (1 << index)) >> index


def get_wav_last_modify_date_time(path_to_wav_file):
    '''
    Return datetime of last modify file
    :param path_to_wav_file: path to the file
    :return: datetime
    '''
    return datetime.datetime.utcfromtimestamp(os.path.getmtime(path_to_wav_file))


def format_phone_call_to_log(date_time, stage_number, answer, phone_number, duration, transcription):
    '''
    Format message to log with phone call values
    :param date_time: datetime of call (used datetime of last modify file)
    :param stage_number: number of stage
    :param answer: answer on stage
    :param phone_number: integer representation of phone number
    :param duration: float duration of call
    :param transcription: transcription of call
    :return: formatted to log message
    '''
    return f"{date_time.date()} {date_time.time()}, <{int(date_time.timestamp())}>, " \
           f"stage: {stage_number}, answer: {answer}, phone_number: +{phone_number}, " \
           f"duration: {duration}, transcription: \"{transcription}\""
