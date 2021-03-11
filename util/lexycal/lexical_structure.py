class LexycalStructure:
    def __init__(self):
        self.__separadores = [";", "[", "]", ")", "(", ")", "{", "}", ",", "=", "."]
        self.__arithmetic_operators = ["-", "+", "/", "*", "^", "++", "--"]
        self.__relational_operators = {
            "=": ["", "="], "!": ["="], ">": ["", "="], "<": ["", "="]
        }
        self.__logical_operators = ["&&", "||", "!"]
        self.__delimiters = [";", ",", ".", "(", ")", "[", "]", "{", "}"]
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

    def get_delimiter(self) -> list[str]:
        return self.__delimiters

    def get_arithmetic_operators(self) -> list[str]:
        return self.__arithmetic_operators

    def get_idk(self) -> list[str]:
        return self.__separadores

    def is_delimiter(self, character: str) -> bool:
        return character in self.__delimiters

    def is_end_lexeme(self, character: str) -> bool:
        """
        Verify if the given character is a delimiter or a whitespace
        :rtype: object
        """
        return self.is_delimiter(character) or character.isspace()

    def is_reserved(self, lexeme: str) -> bool:
        return lexeme in self.__reserved_words

    def is_relational(self, character: str, next_character="") -> [bool, bool]:
        valid_next_chars = self.__relational_operators.get(character)
        if valid_next_chars is not None:
            if next_character in valid_next_chars:
                return True, True
            if "" in valid_next_chars:
                return True, False
        return False, False

    def is_logical(self, character, next_character) -> int:
        if self.__logical_operators.__contains__(character + next_character):
            return 2
        elif self.__logical_operators.__contains__(str(character)):
            return 1
        else:
            return 0

    def is_operator(self, character: str, next_character="") -> int:
        if next_character != "":
            return character + next_character in self.__arithmetic_operators and 2 or 0
        return character in self.__arithmetic_operators and 1 or 0
