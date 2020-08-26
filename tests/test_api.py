import os
import unittest
from grpc._channel import _InactiveRpcError

from recognizer.api import ApiClient
from recognizer.config import Config

from tests.settings import FIRST_WAV, PATH_TO_WAV_FILES


# To avoid day limit while testing api
def make_stubs():
    import json
    stubs = dict()
    c = Config('../configuration.ini')
    api = ApiClient(**c.get_api_credentials())
    wav_files = [[os.path.join(PATH_TO_WAV_FILES, file_name), 0, 0]
                 for file_name in sorted(os.listdir(PATH_TO_WAV_FILES))]
    for wav_file in wav_files:
        response = api.get_stt(wav_file[0])
        stubs[wav_file[0]] = response
    print(stubs)

    with open('stubs.txt', 'wt') as stubs_file:
        json.dump(stubs, stubs_file)


class TestApiClientSetup(unittest.TestCase):
    def test_init_without_credentials(self):
        api = ApiClient(api_key='', secret_key='')
        with self.assertRaises(_InactiveRpcError):
            api.recognize_wav(FIRST_WAV, 1)

    def test_init_bad_credentials(self):
        api = ApiClient(api_key='123', secret_key='456')
        with self.assertRaises(_InactiveRpcError):
            api.recognize_wav(FIRST_WAV, 1)


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        c = Config('../configuration.ini')
        self.api = ApiClient(**c.get_api_credentials(), stubs_filepath='files/stubs.txt')

        # Create list of tuples with: filepath, stage1_response, stage2_response
        self.wav_files = [[os.path.join(PATH_TO_WAV_FILES, file_name), 0, 0]
                          for file_name in sorted(os.listdir(PATH_TO_WAV_FILES))]
        # STAGE One is answerphone?
        self.wav_files[0][1] = 0
        self.wav_files[1][1] = 1
        self.wav_files[2][1] = 1
        self.wav_files[3][1] = 1

        # STAGE Two is comfort?
        self.wav_files[0][2] = 1
        self.wav_files[1][2] = 1
        self.wav_files[2][2] = 1
        self.wav_files[3][2] = 0

    def test_stage_one_is_human(self):
        for wav_file in self.wav_files:
            self.assertEqual(self.api.recognize_wav(wav_file[0], 1), wav_file[1])

    def test_stage_two_is_comfort(self):
        for wav_file in self.wav_files:
            self.assertEqual(self.api.recognize_wav(wav_file[0], 2), wav_file[2])
