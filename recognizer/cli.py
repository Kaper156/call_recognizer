import logging
import argparse
import os.path

logger = logging.getLogger(__name__)


# Used as arg type
def existing_file(value):
    # Check file exist
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError(f'File:"{value}" \t doesn\'t exists')
    return value


# Used as arg type
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


# Used as arg type
def stage(value):
    # Check values
    if value in ['1', '2']:
        return int(value)
    raise argparse.ArgumentTypeError(f'Stage must be 0 or 1:"{value}"')


def parse_args(argv):
    parser = argparse.ArgumentParser()

    # First of all set path to .wav file
    parser.add_argument('-f', dest='filepath', required=True, type=existing_file,
                        help="Path to .wav file")

    # Next step, phone number
    parser.add_argument('-p', action='store', dest='phone', required=True, type=phone,
                        help="Phone number in format: [+]1234567 or [+]123456789012345 "
                             "(Support world standart of length between 7 and 15)")

    # Save to db?
    parser.add_argument('-db', action='store_true', dest='db',
                        help="Flag of using DB (Before using set DB section in configuration.ini)")

    # Stage of recognition .wav
    parser.add_argument('-s', action='store', dest='stage', required=True, type=stage,
                        help="Stage of recognition, now support only: 1 or 2")

    # Set optional parameter name of project which related with call
    parser.add_argument('-p_name', action='store', dest='project_name', type=str,
                        help="Name of project with which phone call will be connected",
                        default="Тестовый проект", required=False)

    # Set optional parameter name of server which related with call
    parser.add_argument('-s_name', action='store', dest='server_name', type=str,
                        help="Name of server with which phone call will be connected",
                        default="Тестовый сервер", required=False)
    # Set optional parameter ip-address of server which related with call
    parser.add_argument('-s_ip', action='store', dest='server_ip', type=str,
                        help="IP of server with which phone call will be connected",
                        default="8.8.8.8", required=False)

    try:
        user_input_arguments = parser.parse_args(argv)
    except argparse.ArgumentTypeError as exc:
        logger.exception(exc)
    logger.debug(f"Got user arguments: {user_input_arguments.__dict__}")
    return user_input_arguments
