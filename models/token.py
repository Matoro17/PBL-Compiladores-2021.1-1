from util.token_types import TokenTypes


class Token:
    def __init__(
            self, lexeme: str, line_number: int, column_number: int, token_type: TokenTypes
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

    def get_token_type(self) -> TokenTypes:
        return self.__token_type

    def __str__(self) -> str:
        return "%i %s %s\n" % (self.__line, self.__token_type.value, self.__lexeme)

    def __repr__(self) -> str:
        return str(self)
