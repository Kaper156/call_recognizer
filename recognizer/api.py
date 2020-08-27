import os

from tinkoff_voicekit_client import ClientSTT

from recognizer.analyzer import TranscriptionAnalyzer

DEFAULT_AUDIO_CONFIG = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}


class ApiClientError(Exception):
    pass


class ApiClient:
    def __init__(self, api_key, secret_key, stubs_filepath=None):
        self.client_stt = ClientSTT(api_key=api_key, secret_key=secret_key)

        # Replace api call to using stubs
        if stubs_filepath:
            self._init_stubs_(stubs_filepath)
            self.get_stt = self._get_stt_STUB_
        else:
            self.get_stt = self._get_stt_real_

    def _get_stt_real_(self, filepath):
        print("Do request to real api")
        filepath = os.path.abspath(filepath)
        response = self.client_stt.recognize(filepath, DEFAULT_AUDIO_CONFIG)
        return response

    def _init_stubs_(self, filepath):
        import json

        with open(filepath, 'rt') as stubs_handler:
            self.STUBS = json.load(stubs_handler)

    def _save_stubs_(self):
        import json
        with open('stubs.txt', 'wt') as stubs_handler:
            json.dump(self.STUBS, stubs_handler)

    def _get_stt_STUB_(self, filepath):
        filepath = os.path.abspath(filepath)
        response = self.STUBS.get(filepath, None)
        if response is None:
            print("File not in stubs! Add it and do request using API")
            response = self._get_stt_real_(filepath)
            self.STUBS[filepath] = response
            self._save_stubs_()
        return response

    def recognize_wav(self, filepath, stage):
        response = self.get_stt(filepath)
        if len(response) == 0:
            # TODO make errors and perform responses
            raise ApiClientError("Something went wrong during request API")
        analyzer = TranscriptionAnalyzer(response)
        return {
            "stage_number": stage,
            "answer": analyzer.analyze_by_stage(stage),
            "transcription": analyzer.get_transcription(),
            "duration": analyzer.get_duration()
        }
