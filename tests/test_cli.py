import unittest
from io import StringIO
from unittest.mock import patch

from recognizer.cli import parse_args

from tests.settings import FIRST_WAV


# TODO change expected dict to Namespace
class TestCliArgParser(unittest.TestCase):
    def setUp(self) -> None:
        self.file = FIRST_WAV
        self.default_argv = [
            '-f', FIRST_WAV,
            '-p', '+74950111255',
            '-db',
            '-s', '1',
            '-s_id', '1',
            '-p_id', '1',
        ]
        self.default_expected = {
            'filepath': FIRST_WAV,
            'phone': 74950111255,
            'db': True,
            'stage': 1,
            'server_id': 1,
            'project_id': 1,
        }

    def test_parse_args_correct_values(self):
        actual = parse_args(self.default_argv)
        self.assertDictEqual(actual.__dict__, self.default_expected)

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

    def test_parse_args_without_server_id(self):
        # delete -s_id parameter and value
        argv = self.default_argv.copy()
        del argv[8]
        del argv[7]

        actual = parse_args(argv)
        self.assertDictEqual(actual.__dict__, self.default_expected)

    def test_parse_args_without_project_id(self):
        # delete -p_id parameter and value
        argv = self.default_argv.copy()
        del argv[10]
        del argv[9]

        actual = parse_args(argv)
        self.assertDictEqual(actual.__dict__, self.default_expected)
