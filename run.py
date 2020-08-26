from recognizer.api import ApiClient
from recognizer.cli import parse_args
from recognizer.config import Config
from recognizer.helpers import get_timestamp_utc, remove_file
from recognizer.logger import log


def main(args):
    # Save timestamp of call program
    timestamp = get_timestamp_utc()
    # Load config (API and DB configuration)
    config = Config('configuration.ini')
    # Init API
    api = ApiClient(**config.get_api_credentials())
    # Get response from API and recognize by stage
    api_response = api.recognize_wav(args.filepath, args.stage)
    # Save to log
    log(args, api_response)  # timestamp
    # If need saving to DB
    if args.db:
        from recognizer.database import DatabaseController
        db = DatabaseController(**config.get_db_config())
        db.save_call_data(**args, result=api_response)  # timestamp
    remove_file(args.filepath)


if __name__ == '__main__':
    import sys

    args = parse_args(sys.argv[1:])
    main(args)
