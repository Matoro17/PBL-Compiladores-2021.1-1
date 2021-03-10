from typing import BinaryIO
from models.token import Token
from controllers.analyzers.lexycal_information import LexycalInformation


class LexycalAnalizer:
    def __init__(self):
        self.__lexycal_info = LexycalInformation()
        self.__errors_list = []

    def get_errors(self) -> list[str]:
        return self.__errors_list

    def start(self, file_pointer: BinaryIO):
        for i in file_pointer.readlines():
            print(i)
            linha = linha + 1
            coluna = 0
            for k in i:
                id_tabela = id_tabela + 1
                coluna = coluna + 1
                print(k)
