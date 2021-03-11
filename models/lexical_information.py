from models.token import Token
from util.lexycal.lexical_states import LexicalStates
from util.token_types import TokenTypes


class LexicalInformation:
    def __init__(self):
        self.__lexeme_builder = []  # int (character) list
        self.state = LexicalStates.NIL
        self.current_line = ""
        self.line_number = 0
        self.column = 0

    def add_character(self, first_character: str, second_character=""):
        self.__lexeme_builder.append(first_character)
        if second_character != "":
            self.__lexeme_builder.append(second_character)

    def generate_token(self, token_type: TokenTypes) -> Token:
        new_token = Token("".join(self.__lexeme_builder), self.line_number, self.column, token_type)
        self.__lexeme_builder.clear()
        self.state = LexicalStates.NIL
        return new_token

    def get_lexeme(self) -> str:
        return "".join(self.__lexeme_builder)
