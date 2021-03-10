from controllers.input_reader import InputReader
from controllers.file_reader import FileReader

if __name__ == "__main__":
    input_reader = InputReader("./input")
    file_reader = FileReader()
    print("OK")
    input_reader.start(file_reader.start)
    print("ERROR")
    # print(lista_erros)
    # print(token_geral)
    # print(tabela_token)
