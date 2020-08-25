from tinkoff_voicekit_client import ClientSTT
from .helpers import read_client_credentials

API_KEY, SECRET_KEY = read_client_credentials()

DEFAULT_AUDIO_CONFIG = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

client = ClientSTT(API_KEY, SECRET_KEY)


def recognize_wav(filepath, stage):
    # TODO this
    # response = client.recognize(filepath, DEFAULT_AUDIO_CONFIG)
    return 1



