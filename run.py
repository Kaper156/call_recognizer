import logging

from recognizer.api import ApiClient
from recognizer.cli import parse_args
from recognizer.config import Config
from recognizer.helpers import get_datetime_now_utc, remove_file


def main(args, run_date_time):
    import recognizer.logger

    # Load config (API and DB configuration)
    config = Config('configuration.ini')

    # Init API
    api = ApiClient(**config.get_api_credentials(), stubs_filepath='./tests/files/stubs.txt')
    # Get response from API and recognize by stage
    api_response = api.recognize_wav(args.filepath, args.stage)

    phone_call_values = {
        'date_time': run_date_time,
        'stage_number': api_response['stage_number'],
        'answer': api_response['answer'],
        'phone_number': args.phone,
        'duration': api_response['duration'],
        'transcription': api_response['transcription']
    }

    # Save result to log file
    recognizer.logger.log_call(**phone_call_values)

    # If need saving to DB
    if args.db:
        # Import controller only if need save data to DB
        from recognizer.database import DatabaseController
        # Init DB controller
        db = DatabaseController(**config.get_db_config())
        # Insert or change instance of phone call
        db.update_or_insert_phone_call(**phone_call_values, project_id=args.project_id, server_id=args.server_id)

    # Remove file when work with him completed
    remove_file(args.filepath)


if __name__ == '__main__':
    import sys

    # After start program save date and time (without TZ)
    run_date_time = get_datetime_now_utc()
    # Parse command line arguments
    args = parse_args(sys.argv[1:])
    # Run main algorithm
    main(args, run_date_time)
