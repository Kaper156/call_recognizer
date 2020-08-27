import datetime
import os


def remove_file(filepath, stub=True):
    if stub:
        print(f"Removing: {filepath}")
    else:
        os.remove(filepath)


def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
    v &= ~mask  # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask  # If x was True, set the bit indicated by the mask.
    return v  # Return the result, we're done.


def get_bit(v, index):
    return (v & (1 << index)) >> index


def get_wav_last_modify_date_time(path_to_wav_file):
    return datetime.datetime.utcfromtimestamp(os.path.getmtime(path_to_wav_file))
