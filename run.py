from recognizer.api import ApiClient
from recognizer.cli import parse_args
from recognizer.config import Config
from recognizer.helpers import remove_file
from recognizer.logger import log


def main(args):
    config = Config('configuration.ini')
    api = ApiClient(**config.get_api_credentials())
    api_response = api.recognize_wav(args.filepath, args.stage)
    log(args, api_response)
    if args.db:
        from recognizer.database import DatabaseController
        db = DatabaseController()
        db.save(args, api_response)
    remove_file(args.filepath)


if __name__ == '__main__':
    import sys

    args = parse_args(sys.argv)
    main(args)
