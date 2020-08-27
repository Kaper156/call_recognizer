import unittest

from recognizer.config import Config
from recognizer.database import DatabaseController
from recognizer.helpers import get_datetime_now_utc

from tests.settings import REAL_CONFIG_FILE


class TestDatabaseControllerConnectionUp(unittest.TestCase):
    def test_connection_up(self):
        cfg = Config(REAL_CONFIG_FILE)
        dbc = DatabaseController(**cfg.get_db_config())
        self.assertIsNotNone(dbc.cur_session)


class TestDatabaseController(unittest.TestCase):
    CLEAR_DB = False

    def setUp(self) -> None:
        cfg = Config(REAL_CONFIG_FILE)
        self.dbc = DatabaseController(**cfg.get_db_config())

    def test_save_call_data_now_first_stage_without_server_and_project(self):
        self.dbc.save_call_data(
            date_time=get_datetime_now_utc(),
            stage=1,
            result=1,
            phone_number=71234567890,
            duration=3.5,
            transcription="Да здравствуйте. Удобно",
        )

    def test_save_call_data_now_first_stage_with_server_and_project(self):
        self.dbc.save_call_data(
            date_time=get_datetime_now_utc(),
            stage=1,
            result=1,
            phone_number=71234567890,
            duration=3.5,
            transcription="Да здравствуйте. Удобно",
            project_name="Тестовый проект №2",
            server_name="Тестовый сервер №2",
            server_ip="192.168.1.1"
        )

    def tearDown(self) -> None:
        if self.CLEAR_DB:
            self.dbc.__clear_db__()
