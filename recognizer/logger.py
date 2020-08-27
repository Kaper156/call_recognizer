import logging

logging.basicConfig(filename='app.log', filemode='w')

r_logger = logging.getLogger('result')
r_logger.setLevel(logging.INFO)

# TODO Maybe set abspath to file
r_file_handler = logging.FileHandler('result.log')
r_file_handler.setFormatter(logging.Formatter("%(asctime)s:%(message)s"))

r_logger.addHandler(r_file_handler)


def log_call(date_time,
             stage_number, answer,
             phone_number, duration,
             transcription):
    r_logger.info(f"{date_time.date()} {date_time.time()}, <{int(date_time.timestamp())}>, "
                  f"stage: {stage_number} = {answer}, "
                  f"phone_number: +{phone_number}, duration: {duration},"
                  f"transcription: \"{transcription}\"")
