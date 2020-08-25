import os
import os.path
import unittest

from recognizer.config import Config
from tests.settings import BAD_CONFIG_FILE, API_KEY, SECRET_KEY


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.exist_config_file_path = BAD_CONFIG_FILE
        self.not_exist_config_file_path = self.exist_config_file_path + '.not_exist'

    def test_config_file_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            c = Config(config_file_path=self.not_exist_config_file_path)
            self.assertTrue(os.path.exists(self.not_exist_config_file_path))

    def test_config_file_exist_api(self):
        config = Config(self.exist_config_file_path)
        credentials = config.get_api_credentials()
        self.assertEqual(credentials['api_key'], API_KEY)
        self.assertEqual(credentials['secret_key'], SECRET_KEY)

    def tearDown(self) -> None:
        if os.path.exists(self.not_exist_config_file_path):
            os.remove(self.not_exist_config_file_path)
