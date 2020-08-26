import os.path
import configparser


class Config:
    def __init__(self, config_file_path):
        self.filepath = config_file_path
        self.parser = configparser.ConfigParser()
        if not os.path.exists(config_file_path):
            self._write_config_()
            raise FileNotFoundError("File not found. Parser create .ini file, please set parameters.")
        self.parser.read(config_file_path)

    def _write_config_(self):
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
