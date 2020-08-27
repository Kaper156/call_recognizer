import unittest

from recognizer.config import Config
from recognizer.database import PostgresDatabaseController, update_or_insert_phone_call
from recognizer.helpers import get_datetime_now_utc

from tests.settings import REAL_CONFIG_FILE


class TestPostgresDatabaseControllerConnectionUp(unittest.TestCase):
    def test_connection_up(self):
        cfg = Config(REAL_CONFIG_FILE)
        try:
            dbc = PostgresDatabaseController(**cfg.get_db_config())
        except Exception as exc:
            self.fail(exc)


class Test_update_or_insert_phone_call(unittest.TestCase):
    CLEAR_DB = False

    def setUp(self) -> None:
        cfg = Config(REAL_CONFIG_FILE)
        self.dbc = PostgresDatabaseController(**cfg.get_db_config())

        self.phone_call_data = {
            'date_time': get_datetime_now_utc(),
            'stage_number': 1,
            'answer': 1,
            'phone_number': 71234567890,
            'duration': 3.5,
            'transcription': 'Да здравствуйте. Удобно',
            'project_name': 'Тестовый проект#2',
            'server_name': 'Тестовый сервер#2',
            'server_ip': '127.0.0.1',
        }

    def test_correct_phone_call_without_project_and_server(self):
        try:
            with self.dbc as session:
                update_or_insert_phone_call(session=session, **self.phone_call_data)
        except Exception as exc:
            self.fail(exc)

    def tearDown(self) -> None:
        if self.CLEAR_DB:
            self.dbc.__clear_db__()
