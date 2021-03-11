class LexycalStructure:
    def __init__(self):
        self.__separadores = [";", "[", "]", ")", "(", ")", "{", "}", ",", "=", "."]
        self.__operadores = ["-", "+", "/", "*", "^"]
        self.__delimeters = [";"]
        self.__reserved_words = [
            "int",
            "float",
            "char",
            "if",
            "else",
            "printf",
            "for",
            "while",
            "return",
            "continue",
            "break",
            "read",
        ]

    def get_reserved_words(self) -> list[str]:
        return self.__reserved_words

    def get_delimeters(self) -> list[str]:
        return self.__delimeters

    def get_operators(self) -> list[str]:
        return self.__operadores

    def get_idk(self) -> list[str]:
        return self.__separadores
