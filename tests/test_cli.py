import unittest
from io import StringIO
from argparse import Namespace
from unittest.mock import patch

from recognizer.cli import parse_args

from tests.settings import FIRST_WAV


class TestCliArgParser(unittest.TestCase):
    def setUp(self) -> None:
        self.file = FIRST_WAV
        self.default_argv = [
            '-f', FIRST_WAV,
            '-p', '+74950111255',
            '-db',
            '-s', '1',
            '-p_name', 'Тестовый проект №1',
            '-s_name', 'Тестовый сервер №1',
            '-s_ip', '1.1.1.1',

        ]
        self.default_expected = {
            'filepath': FIRST_WAV,
            'phone': 74950111255,
            'db': True,
            'stage': 1,
            'project_name': 'Тестовый проект №1',
            'server_name': 'Тестовый сервер №1',
            'server_ip': '1.1.1.1',

        }
        self.default_expected_namespace = Namespace(**self.default_expected)

    def test_parse_args_correct_values_stage_1(self):
        actual = parse_args(self.default_argv)
        self.assertEqual(actual, self.default_expected_namespace)

    def test_parse_args_correct_values_stage_2(self):
        argv = self.default_argv.copy()
        argv[6] = '2'
        actual = parse_args(argv)

        expected = self.default_expected.copy()
        expected['stage'] = 2

        self.assertEqual(actual, Namespace(**expected))

    @patch('sys.stderr', new_callable=StringIO)
    def test_parse_args_file_doesnt_exists(self, mock_stderr):
        argv = self.default_argv.copy()
        argv[1] = FIRST_WAV + '.not_exist'
        with self.assertRaises(SystemExit):
            parse_args(argv)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"File.*doesn\'t exists")

    @patch('sys.stderr', new_callable=StringIO)
    def test_parse_args_phone_number_length_16(self, mock_stderr):
        argv = self.default_argv.copy()
        # make number with length 16 digits
        argv[3] = "+1234567890123456"
        with self.assertRaises(SystemExit):
            parse_args(argv)
        self.assertRegexpMatches(mock_stderr.getvalue(), r".*(number length greater than maximum length).*")

    @patch('sys.stderr', new_callable=StringIO)
    def test_parse_args_phone_number_length_6(self, mock_stderr):
        argv = self.default_argv.copy()
        # make number with length 6 digits
        argv[3] = "+123456"
        with self.assertRaises(SystemExit):
            parse_args(argv)
        self.assertRegexpMatches(mock_stderr.getvalue(), r".*(number length less than minimum length).*")

    @patch('sys.stderr', new_callable=StringIO)
    def test_parse_args_phone_number_have_other_symbols(self, mock_stderr):
        argv = self.default_argv.copy()
        # replace 7 and s
        argv[3] = argv[3].replace('7', 's')
        with self.assertRaises(SystemExit):
            parse_args(argv)
        self.assertRegexpMatches(mock_stderr.getvalue(), r".*(number have other symbols).*")

    @patch('sys.stderr', new_callable=StringIO)
    def test_parse_args_stage_incorrect_string_value(self, mock_stderr):
        argv = self.default_argv.copy()
        # make number with length 16 digits
        argv[6] = "One"
        with self.assertRaises(SystemExit):
            parse_args(argv)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"Stage must be 0 or 1:.*")

    @patch('sys.stderr', new_callable=StringIO)
    def test_parse_args_stage_incorrect_int_value_three(self, mock_stderr):
        argv = self.default_argv.copy()
        # make number with length 16 digits
        argv[6] = '3'
        with self.assertRaises(SystemExit):
            parse_args(argv)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"Stage must be 0 or 1:.*")

    @patch('sys.stderr', new_callable=StringIO)
    def test_parse_args_stage_incorrect_int_value_negative_one(self, mock_stderr):
        argv = self.default_argv.copy()
        # make number with length 16 digits
        argv[6] = '-1'
        with self.assertRaises(SystemExit):
            parse_args(argv)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"Stage must be 0 or 1:.*")

    def test_parse_args_without_db(self):
        expected = self.default_expected.copy()
        expected['db'] = False

        # delete -d parameter
        argv = self.default_argv.copy()
        del argv[4]

        actual = parse_args(argv)
        self.assertDictEqual(actual.__dict__, expected)

    def test_parse_args_without_server_name_and_ip(self):
        # delete -s_id parameter and value
        argv = self.default_argv.copy()
        del argv[12]
        del argv[11]

        del argv[10]
        del argv[9]

        # Expect default for arg server_name, server_ip
        expected = self.default_expected.copy()
        expected['server_name'] = 'Тестовый сервер'
        expected['server_ip'] = '8.8.8.8'

        expected_namespace = Namespace(**expected)
        actual = parse_args(argv)
        self.assertEqual(actual, expected_namespace)

    def test_parse_args_without_project_name(self):
        # delete -p_id parameter and value
        argv = self.default_argv.copy()
        del argv[8]
        del argv[7]

        # Expect default for arg project_name
        expected = self.default_expected.copy()
        expected['project_name'] = 'Тестовый проект'

        expected_namespace = Namespace(**expected)
        actual = parse_args(argv)
        self.assertEqual(actual, expected_namespace)
