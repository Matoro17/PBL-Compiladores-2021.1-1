class LexicalStructure:
    def __init__(self):
        self.__arithmetic_operators = {
            "-": ["", "-"],
            "+": ["", "+"],
            "/": [""],
            "*": [""],
            "^": [""],
        }
        self.__relational_operators = {
            "=": ["", "="],
            "!": ["="],
            ">": ["", "="],
            "<": ["", "="],
        }
        self.__logical_operators = {"&": ["&"], "|": ["|"], "!": [""]}
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
            "write",
        ]

    def get_reserved_words(self) -> list[str]:
        return self.__reserved_words

    def get_delimiter(self) -> list[str]:
        return self.__delimiters

    def is_delimiter(self, character: str) -> bool:
        return character in self.__delimiters

    def is_end_lexeme(self, character: str) -> bool:
        """
        Verify if the given character is a delimiter or a whitespace
        :rtype: object
        """
        return (
                self.is_delimiter(character)
                or character.isspace()
                or character == ""
                or self.is_relational(character)[0]
                or self.is_logical(character)[0]
                or self.is_arithmetic(character)[0]
        )

    def is_reserved(self, lexeme: str) -> bool:
        return lexeme in self.__reserved_words

    @staticmethod
    def __is_in_list_dict(
            search_in: dict[str, list[str]], character: str, next_character=""
    ) -> [bool, bool]:
        valid_next_chars = search_in.get(character)
        if valid_next_chars is not None:
            if next_character in valid_next_chars:
                return True, True
            if "" in valid_next_chars:
                return True, False
        return False, False

    def is_relational(self, character: str, next_character="") -> [bool, bool]:
        return self.__is_in_list_dict(
            self.__relational_operators, character, next_character
        )

    def is_logical(self, character: str, next_character="") -> [bool, bool]:
        return self.__is_in_list_dict(
            self.__logical_operators, character, next_character
        )

    def is_arithmetic(self, character: str, next_character="") -> [bool, bool]:
        return self.__is_in_list_dict(
            self.__arithmetic_operators, character, next_character
        )
