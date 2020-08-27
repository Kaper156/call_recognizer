import os
import shutil

from recognizer.api import ApiClient
from recognizer.config import Config

from tests.settings import PATH_TO_WAV_FILES, PATH_TO_WAV_FILES_COPY, REAL_CONFIG_FILE, STUBS_API_FILE


def copy_wav_files():
    # Make dir for copy files
    if not os.path.exists(PATH_TO_WAV_FILES_COPY):
        os.mkdir(PATH_TO_WAV_FILES_COPY)

    # Copy each file
    for wav_file in os.listdir(PATH_TO_WAV_FILES):
        src = os.path.join(PATH_TO_WAV_FILES, wav_file)
        dest = os.path.join(PATH_TO_WAV_FILES_COPY, wav_file)
        if not os.path.exists(dest):
            shutil.copy(src, dest)


def make_stubs_for_api():
    # To avoid day limit while testing api
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

    with open(STUBS_API_FILE, 'wt') as stubs_file:
        json.dump(stubs, stubs_file)
