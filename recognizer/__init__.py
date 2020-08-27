import logging

# Logger for application
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# File handler
logger_handler = logging.FileHandler('app.log', )
logger_handler.setLevel(logging.DEBUG)
# Format
logger_formatter = logging.Formatter('%(asctime)s [%(levelname)s]| %(name)s: %(message)s',
                                     "%Y-%m-%d %H:%M:%S")
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

# Logger for results
result_logger = logging.getLogger('result')
result_logger.setLevel(logging.INFO)
# File handler
result_logger_handler = logging.FileHandler('result.log', )
result_logger_handler.setLevel(logging.INFO)
# Format
result_logger_formatter = logging.Formatter('%(asctime)s| %(message)s',
                                            "%Y-%m-%d %H:%M:%S")
result_logger_handler.setFormatter(result_logger_formatter)
result_logger.addHandler(result_logger_handler)
