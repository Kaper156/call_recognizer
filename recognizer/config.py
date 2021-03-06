import logging
import os.path
import configparser

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, config_file_path):
        '''
        Used to get credentials for API and connection string to Database
        :param config_file_path: path to *.ini file of project
        '''
        self.filepath = config_file_path
        self.parser = configparser.ConfigParser()
        # If user start program without path to config or config is not exist
        if not os.path.exists(config_file_path):
            # Write empty config at this path
            self._write_empty_config_()
            logger.critical("Error while loading config. Empty config created.")
            exit(1)
        self.parser.read(config_file_path)
        logger.debug(f"Successfully read cfg from: {config_file_path}")

    def _write_empty_config_(self):
        '''
        Write at self.filepath empty config file
        :return: None
        '''
        # Clear parser
        self.parser = configparser.ConfigParser()

        self.parser.add_section('API')
        self.parser['API']['api_key'] = ''
        self.parser['API']['secret_key'] = ''

        self.parser.add_section('DB')
        self.parser['DB']['host'] = ''
        self.parser['DB']['port'] = ''
        self.parser['DB']['database'] = ''
        self.parser['DB']['user'] = ''
        self.parser['DB']['password'] = ''

        with open(self.filepath, 'w') as file_handler:
            self.parser.write(file_handler)
        logger.debug(f"Write empty config to: {self.filepath}")

    def get_api_credentials(self):
        return {
            'api_key': self.parser['API']['api_key'],
            'secret_key': self.parser['API']['secret_key'],
        }

    def get_db_config(self):
        return {
            'user': self.parser['DB']['user'],
            'password': self.parser['DB']['password'],
            'host': self.parser['DB']['host'],
            'port': self.parser['DB']['port'],
            'database': self.parser['DB']['database'],
        }
