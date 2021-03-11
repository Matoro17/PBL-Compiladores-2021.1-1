class LexycalStructure:
    def __init__(self):
        self.__separadores = [";", "[", "]", ")", "(", ")", "{", "}", ",", "=", "."]
        self.__operadores = ["-", "+", "/", "*", "^", "++", "--"]
        self.__operadores_rel = ["==", "!=", ">", ">=", "<", "<=", "="]
        self.__operadores_log = ["&&", "||", "!"]
        self.__delimeters = [";", ",", ".", "(", ")", "[", "]", "{", "}"]
        self.__reserved_words = [
            "var",
            "const",
            "typedef",
            "struct",
            "extends",
            "procedure",
            "function",
            "start",
            "return",
            "if",
            "else",
            "then",
            "while",
            "read",
            "print",
            "int",
            "real",
            "boolean",
            "string",
            "true",
            "false",
            "global",
            "local",
            "float",
            "write"
        ]

    def get_reserved_words(self) -> list[str]:
        return self.__reserved_words

    def get_delimeters(self) -> list[str]:
        return self.__delimeters

    def get_operators(self) -> list[str]:
        return self.__operadores

    def get_idk(self) -> list[str]:
        return self.__separadores

    def is_delimiter(self, character) -> bool:
        return self.__delimeters.__contains__(character)

    def is_reserved(self, lexeme: str) -> bool:
        return self.__reserved_words.__contains__(lexeme)

    def is_relational(self, character, next_character) -> int:
        if self.__operadores_rel.__contains__(character + next_character):
            return 2
        elif self.__operadores_rel.__contains__(character):
            return 1
        else:
            return 0

    def is_logical(self, character, next_character) -> int:
        if self.__operadores_log.__contains__(character + next_character):
            return 2
        elif self.__operadores_log.__contains__(str(character)):
            return 1
        else:
            return 0

    def is_operator(self, character, next_character) -> int:
        if self.__operadores.__contains__(character + next_character):
            return 2
        elif self.__operadores.__contains__(character):
            return 1
        else:
            return 0
