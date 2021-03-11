from typing import BinaryIO

from models.lexical_information import LexicalInformation
from util.lexycal.lexical_states import LexicalStates
from util.token_types import TokenTypes


class LexicalAnalyzer:
    def __init__(self):
        self.__lexical_info = LexicalInformation()
        self.__tokens = []
        self.__errors_list = []

    def get_errors(self) -> list[str]:
        return self.__errors_list

    def __block_comment_state(self, previous_character: str, character: str):
        self.__lexical_info.add_character(character)
        if character == "/" and previous_character == "*":
            self.__lexical_info.state = LexicalStates.NIL
            self.__tokens.append(
                self.__lexical_info.generate_token(TokenTypes.BLOCK_COMMENT)
            )

    def __parse_line(self, line_data: bytes):
        previous_character = ""
        for column in range(0, len(line_data)):
            self.__lexical_info.column = column + 1
            character = line_data[column]
            # print(
            #    len(line_data), line_data.replace(" ", "").replace("\n", "\\n"),
            #    "PRE '%s'" % previous_character,
            #    "CUR '%s'" % character.replace("\n", "\\n"),
            #    self.__lexical_info.state
            # )
            if self.__lexical_info.state == LexicalStates.NIL:
                # Start point, verify first character in lexeme
                if previous_character == "/" and character == "*":
                    print("line_data", line_data)
                    self.__lexical_info.add_character(previous_character, character)
                    self.__lexical_info.state = LexicalStates.BLOCK_COMMENT
            elif self.__lexical_info.state == LexicalStates.BLOCK_COMMENT:
                self.__block_comment_state(previous_character, str(character))
            column += 1
            previous_character = character
        if self.__lexical_info.state != LexicalStates.NIL:
            if self.__lexical_info.state == LexicalStates.STRING:
                self.__errors_list.append(
                    self.__lexical_info.generate_token(TokenTypes.MALFORMED_STRING)
                )
            if self.__lexical_info.state != LexicalStates.BLOCK_COMMENT:
                self.__lexical_info.generate_token(TokenTypes.MALFORMED_COMMENT)

    def start(self, file_pointer: BinaryIO):
        line_number = 0
        for current_line in file_pointer.readlines():
            self.__lexical_info.line_number = line_number + 1
            self.__parse_line(current_line)
            line_number += 1
        if self.__lexical_info.state == LexicalStates.BLOCK_COMMENT:
            self.__errors_list.append(self.__lexical_info.generate_token(TokenTypes.MALFORMED_COMMENT))
        print(self.__tokens)
        print(self.__errors_list)
