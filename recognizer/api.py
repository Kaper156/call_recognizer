import logging
import os

from tinkoff_voicekit_client import ClientSTT

from recognizer.analyzer import TranscriptionAnalyzer

logger = logging.getLogger(__name__)

DEFAULT_AUDIO_CONFIG = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}


# To catch any API errors
class ApiClientError(Exception):
    pass


class ApiClient:
    def __init__(self, api_key, secret_key, stubs_filepath=None):
        '''
        Initialize ClientSTT by api and secret keys. If stubs is set used them when file is known
        :param api_key: API KEY
        :param secret_key: SECRET KEY
        :param stubs_filepath: path to json file with stubs (which is a dict with keys - filepaths and values - responses)
        '''
        self.client_stt = ClientSTT(api_key=api_key, secret_key=secret_key)

        # Replace api call to using stubs
        if stubs_filepath:
            self._init_stubs_(stubs_filepath)
            self.get_stt = self._get_stt_STUB_
            logger.debug(f"API connected to stubs-file:{stubs_filepath}")
        else:
            self.get_stt = self._get_stt_real_
            logger.debug(f"API used real request to server:{stubs_filepath}")

    def _get_stt_real_(self, filepath):
        # Do response to real server
        logger.debug(f"API send to real server this file:{filepath}")
        filepath = os.path.abspath(filepath)
        response = self.client_stt.recognize(filepath, DEFAULT_AUDIO_CONFIG)
        return response

    def _init_stubs_(self, filepath):
        # Load stubs
        import json

        with open(filepath, 'rt') as stubs_handler:
            self.STUBS = json.load(stubs_handler)
        logger.debug("Stubs loaded")

    def _save_stubs_(self):
        # Save changes in stubs
        import json
        with open('stubs.txt', 'wt') as stubs_handler:
            json.dump(self.STUBS, stubs_handler)
        logger.debug("Stub file updated.")

    def _get_stt_STUB_(self, filepath):
        # Try to get response for filepath from stubs
        filepath = os.path.abspath(filepath)
        response = self.STUBS.get(filepath, None)
        # Response not found in stubs
        if response is None:
            logger.debug("File not in stubs! Add it and do request using API")
            response = self._get_stt_real_(filepath)
            self.STUBS[filepath] = response
            # Save new file and its response
            self._save_stubs_()
        return response

    def recognize_wav(self, filepath, stage):
        '''
        Get response about filepath from api and analyze it
        :param filepath: path to wav file
        :param stage: stage to analyze
        :return: data about recognizing
        '''
        response = self.get_stt(filepath)
        if len(response) == 0:
            raise ApiClientError("Something went wrong during request API")
        analyzer = TranscriptionAnalyzer(response)
        return {
            "stage_number": stage,
            "answer": analyzer.analyze_by_stage(stage),
            "transcription": analyzer.get_transcription(),
            "duration": analyzer.get_duration()
        }
