import os.path

# Wav files
PATH_TO_WAV_FILES = os.path.abspath('./files/wav')
PATH_TO_WAV_FILES_COPY = os.path.abspath('./files/copy_wav')
FIRST_WAV = os.path.relpath(os.path.join(PATH_TO_WAV_FILES, '1.wav'))

# Config
BAD_CONFIG_FILE = 'files/bad_config.ini'
REAL_CONFIG_FILE = '../configuration.ini'
API_KEY = 'test_api_key'
SECRET_KEY = 'most_secret_key'
