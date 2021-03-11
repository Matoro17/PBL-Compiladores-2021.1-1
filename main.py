from controllers.file_reader import FileReader
from controllers.input_reader import InputReader

if __name__ == "__main__":
    input_reader = InputReader("./input")
    file_reader = FileReader()
    input_reader.start(file_reader.start)
    # print(lista_erros)
    # print(token_geral)
    # print(tabela_token)
