class Token:
    def __init__(
        self, lexeme: str, line_number: int, column_number: int, token_type: str
    ):
        self.__lexeme = lexeme
        self.__line = line_number
        self.__column = column_number
        self.__token_type = token_type

    def get_lexeme(self) -> str:
        return self.__lexeme

    def get_line(self) -> int:
        return self.__line

    def get_column(self) -> int:
        return self.__column

    def get_token_type(self) -> str:
        return self.__token_type
