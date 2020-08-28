import os
import os.path
import shutil
import unittest

from recognizer.helpers import remove_file, set_bit, get_bit
from tests.settings import FIRST_WAV, PATH_TO_WAV_FILES_COPY


class TestRemoveFile(unittest.TestCase):
    def setUp(self) -> None:
        file_name = "delete_me.wav"
        self.file_path = os.path.join(PATH_TO_WAV_FILES_COPY, file_name)
        if not os.path.exists(self.file_path):
            shutil.copy(FIRST_WAV, self.file_path)

    def test_remove_file_with_stub(self):
        remove_file(self.file_path, stub=True)
        if not os.path.exists(self.file_path):
            self.fail()

    def test_remove_file_without_stub(self):
        remove_file(self.file_path, stub=False)
        if os.path.exists(self.file_path):
            self.fail()


class TestBitOperations(unittest.TestCase):
    def setUp(self) -> None:
        self.one_and_four_null = 0b1000

    def test_set_bit_after_number(self):
        expected = 0b11000
        actual = set_bit(self.one_and_four_null, 4, 1)
        print(f"{expected:b} == {actual:b}")
        self.assertEqual(actual, expected)

    def test_set_bit_before_number(self):
        expected = 0b1001
        actual = set_bit(self.one_and_four_null, 0, 1)
        print(f"{expected:b} == {actual:b}")
        self.assertEqual(actual, expected)

    def test_get_bit_first(self):
        expected = 1
        actual = get_bit(self.one_and_four_null, 3)
        print(f"{expected:b} == {actual:b}")
        self.assertEqual(actual, expected)

    def test_get_bit_last(self):
        expected = 0
        actual = get_bit(self.one_and_four_null, 0)
        print(f"{expected:b} == {actual:b}")
        self.assertEqual(actual, expected)