from recognizer.api import recognize_wav
from recognizer.helpers import remove_file
from recognizer.logger import log


def is_valid_args(args):
    return True


def main(args):
    api_response = recognize_wav(args.filepath, args.stage)
    log(args, api_response)
    if args.db:
        from recognizer.database import DatabaseController
        db = DatabaseController()
        db.save(args, api_response)
    remove_file(args.filepath)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    # First of all set path to .wav file
    parser.add_argument('-f', action='store', dest='filepath', required=True)

    # Next step, phone number
    parser.add_argument('-p', action='store', dest='phone', required=True)

    # Save to db?
    # TODO check by regex
    parser.add_argument('-db', action='store', dest='db', required=True)

    # Stage of recognition .wav
    parser.add_argument('-s', action='store', dest='stage', required=True)
    args = parser.parse_args()
    if not is_valid_args(args):
        exit(1)
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)
