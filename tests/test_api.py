import os
import unittest
import copy

from grpc._channel import _InactiveRpcError

from recognizer.api import ApiClient
from recognizer.config import Config

from tests.settings import FIRST_WAV, PATH_TO_WAV_FILES, REAL_CONFIG_FILE


# To avoid day limit while testing api
def make_stubs():
    import json
    stubs = dict()
    c = Config(REAL_CONFIG_FILE)
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
        c = Config(REAL_CONFIG_FILE)
        self.api = ApiClient(**c.get_api_credentials(), stubs_filepath='files/stubs.txt')

        # Create list of tuples with: filepath, stage1_response, stage2_response
        self.wav_files = list(os.path.abspath(os.path.join(PATH_TO_WAV_FILES, rel_filepath))
                              for rel_filepath in sorted(os.listdir(PATH_TO_WAV_FILES)))
        expected_without_stages = {
            self.wav_files[0]: {
                "transcription": 'вас приветствует автоответчик оставьте сообщение после сигнала',
                "duration": 5.7
            },
            self.wav_files[1]: {
                "transcription": 'алло говорите',
                "duration": 3.3
            },
            self.wav_files[2]: {
                "transcription": 'ну да удобно его слушаю',
                "duration": 4.5
            },
            self.wav_files[3]: {
                "transcription": 'нет я сейчас на работе до свидания',
                "duration": 3.9
            }
        }

        # Set expected on first stage
        self.expected_on_stage1 = copy.deepcopy(expected_without_stages)
        # Set stage_number
        self.expected_on_stage1[self.wav_files[0]]['stage_number'] = 1
        self.expected_on_stage1[self.wav_files[1]]['stage_number'] = 1
        self.expected_on_stage1[self.wav_files[2]]['stage_number'] = 1
        self.expected_on_stage1[self.wav_files[3]]['stage_number'] = 1

        # Set answer
        self.expected_on_stage1[self.wav_files[0]]['answer'] = 0
        self.expected_on_stage1[self.wav_files[1]]['answer'] = 1
        self.expected_on_stage1[self.wav_files[2]]['answer'] = 1
        self.expected_on_stage1[self.wav_files[3]]['answer'] = 1

        # Set expected on first stage
        self.expected_on_stage2 = copy.deepcopy(expected_without_stages)
        # Set stage_number
        self.expected_on_stage2[self.wav_files[0]]['stage_number'] = 2
        self.expected_on_stage2[self.wav_files[1]]['stage_number'] = 2
        self.expected_on_stage2[self.wav_files[2]]['stage_number'] = 2
        self.expected_on_stage2[self.wav_files[3]]['stage_number'] = 2

        # Set answer
        self.expected_on_stage2[self.wav_files[0]]['answer'] = 1
        self.expected_on_stage2[self.wav_files[1]]['answer'] = 1
        self.expected_on_stage2[self.wav_files[2]]['answer'] = 1
        self.expected_on_stage2[self.wav_files[3]]['answer'] = 0

    def test_stage_1_is_human(self):
        for path_to_wav_file, expected in self.expected_on_stage1.items():
            actual = self.api.recognize_wav(path_to_wav_file, 1)
            self.assertDictEqual(actual, expected)

    def test_stage_2_is_comfort(self):
        for path_to_wav_file, expected in self.expected_on_stage2.items():
            actual = self.api.recognize_wav(path_to_wav_file, 2)
            self.assertDictEqual(actual, expected)
