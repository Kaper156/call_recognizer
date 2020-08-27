import datetime
import os


def remove_file(filepath, stub=True):
    if stub:
        print(f"Removing: {filepath}")
    else:
        os.remove(filepath)


def get_datetime_now_utc():
    return datetime.datetime.utcnow()


def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
    v &= ~mask  # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask  # If x was True, set the bit indicated by the mask.
    return v  # Return the result, we're done.


def get_bit(v, index):
    return (v & (1 << index)) >> index
