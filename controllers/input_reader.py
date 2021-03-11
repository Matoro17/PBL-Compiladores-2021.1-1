import os
from collections.abc import Callable
from os.path import isfile, join
from pathlib import Path


class InputReader:
    def __init__(self, input_directory: str):
        self.__source_directory = input_directory

    def start(self, read_file_callback: Callable[[str], bool]) -> bool:
        all_success = True
        if os.path.exists(self.__source_directory):
            for filename in os.listdir(self.__source_directory):
                complete_filename = join(self.__source_directory, filename)
                if isfile(complete_filename) and complete_filename.endswith(".txt"):
                    all_success = read_file_callback(complete_filename)
        return all_success
