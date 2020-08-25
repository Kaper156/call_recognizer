import os
import shutil

from tests.settings import PATH_TO_WAV_FILES, PATH_TO_WAV_FILES_COPY


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


