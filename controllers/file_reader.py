from typing import BinaryIO
from controllers.analyzers import singletone_lexycal


class FileReader:
    def __init__(self):
        self.__file_pointer = BinaryIO()

    def open_file(self, file_path: str) -> bool:
        """Abre o arquivo de entrada"""
        print("Opening input file %s" % file_path)
        try:
            self.__file_pointer = open(file_path, "r")
        except Exception as e:
            print(e)
            return False
        return True

    def start(self, filename: str) -> bool:
        if self.open_file(filename):
            singletone_lexycal.start(self.__file_pointer)
            return True

        print("Error on reading file %s" % filename)
        return False
