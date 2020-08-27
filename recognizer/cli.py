import argparse
import os.path
import logging


import recognizer.logger


def existing_file(value):
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError(f'File:"{value}" \t doesn\'t exists')
    return value


def phone(value):
    # Delete plus
    if value[0] == '+':
        value = value[1:]

    # Check for other symbols by conversation number to int
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f'Incorrect phone number (number have other symbols):"{value}"')

    # Check phone length
    if len(str(value)) > 15:
        raise argparse.ArgumentTypeError(f'Incorrect phone number '
                                         f'(number length greater than maximum length):"{value}"')
    elif len(str(value)) < 7:
        raise argparse.ArgumentTypeError(f'Incorrect phone number '
                                         f'(number length less than minimum length):"{value}"')

    return value


def stage(value):
    # Check values
    # TODO fix to 1 and 2
    if value in ['0', '1']:
        return int(value)
    raise argparse.ArgumentTypeError(f'Stage must be 0 or 1:"{value}"')


def parse_args(argv):
    parser = argparse.ArgumentParser()

    # First of all set path to .wav file
    parser.add_argument('-f', dest='filepath', required=True, type=existing_file)

    # Next step, phone number
    parser.add_argument('-p', action='store', dest='phone', required=True, type=phone)

    # Save to db?
    parser.add_argument('-db', action='store_true', dest='db', )

    # Stage of recognition .wav
    parser.add_argument('-s', action='store', dest='stage', required=True, type=stage)

    # Set optional parameter id of project which related with call
    parser.add_argument('-p_id', action='store', dest='project_id', type=int, default=1, required=False)

    # Set optional parameter id of server which related with call
    parser.add_argument('-s_id', action='store', dest='server_id', type=int, default=1, required=False)

    try:
        args = parser.parse_args(argv)
    except argparse.ArgumentTypeError as exc:
        logging.exception(exc)
        exit(1)

    return args
