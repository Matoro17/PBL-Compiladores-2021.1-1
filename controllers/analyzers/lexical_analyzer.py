from typing import BinaryIO
from models.lexical_information import LexicalInformation
from util.lexycal.lexical_states import LexicalStates
from util.lexycal.lexical_structure import LexycalStructure
from util.token_types import TokenTypes


class LexicalAnalyzer:
    def __init__(self):
        self.__lexical_info = LexicalInformation()
        self.__lexical_structure = LexycalStructure()
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

    def __line_comment_state(self, character):
        self.__lexical_info.add_character(character)
        if character == "\n":
            self.__lexical_info.state = LexicalStates.NIL
            self.__tokens.append(
                self.__lexical_info.generate_token(TokenTypes.LINE_COMMENT)
            )

    def __string_state(self, character: str):
        self.__lexical_info.add_character(character)
        if character == "\"":
            self.__lexical_info.state = LexicalStates.NIL
            self.__tokens.append(
                self.__lexical_info.generate_token(TokenTypes.STRING)
            )

    def __number_state(self, character):
        self.__lexical_info.add_character(character)
        if 48 <= ord(character) <= 57:
            self.__lexical_info.state = LexicalStates.NIL
            self.__tokens.append(
                self.__lexical_info.generate_token(TokenTypes.NUMBER)
            )

    def __delimiter_state(self, character):
        self.__lexical_info.add_character(character)
        self.__tokens.append(
            self.__lexical_info.generate_token(TokenTypes.DELIMITER)
        )

    def __is_character_indentifier(self, character):
        return 48 <= ord(character) <= 57 \
               or ord(character) == 95 \
               or 65 <= ord(character) <= 90 \
               or 97 <= ord(character) <= 122

    def __identifier_state(self, character, next_character):
        if self.__is_character_indentifier(character):
            self.__lexical_info.add_character(character)
        elif character == " " or character == ";" or character == "\n":
            self.__lexical_info.state = LexicalStates.NIL
            if self.__lexical_structure.is_reserved(self.__lexical_info.get_lexeme()):
                self.__tokens.append(
                    self.__lexical_info.generate_token(TokenTypes.RESERVED_WORD)
                )
            else:
                self.__tokens.append(
                    self.__lexical_info.generate_token(TokenTypes.IDENTIFIER)
                )
        else:
            self.__lexical_info.add_character(character)
            self.__errors_list.append(
                self.__lexical_info.generate_token(TokenTypes.INVALID_SYMBOL)
            )

    def __logical_ope_state(self, character, next_character):
        if self.__lexical_structure.is_logical(character, next_character) == 1:
            self.__lexical_info.add_character(character)
        elif self.__lexical_structure.is_logical(character, next_character) == 2:
            self.__lexical_info.add_character(character, next_character)
        self.__tokens.append(
            self.__lexical_info.generate_token(TokenTypes.LOGIC_OPERATOR)
        )

    def __lexical_ope_state(self, character, next_character):
        if self.__lexical_structure.is_relational(character, next_character) == 1:
            self.__lexical_info.add_character(character)
        elif self.__lexical_structure.is_relational(character, next_character) == 2:
            self.__lexical_info.add_character(character, next_character)
        self.__tokens.append(
            self.__lexical_info.generate_token(TokenTypes.RELATIONAL_OPERATOR)
        )

    def __parse_line(self, line_data: bytes):
        previous_character = ""
        next_character = ""
        for column in range(0, len(line_data)):
            self.__lexical_info.column = column + 1
            character = line_data[column]
            if column + 1 < len(line_data):
                next_character = line_data[column + 1]
            else:
                next_character = ""
            #print(
            #   len(line_data), line_data.replace(" ", "").replace("\n", "\\n"),
            #   "PRE '%s'" % previous_character,
            #   "CUR '%s'" % character.replace("\n", "\\n"),
            #   self.__lexical_info.state
            #)
            if self.__lexical_info.state == LexicalStates.NIL:
                # Start point, verify first character in lexeme
                if character == "/" and next_character == "*":
                    self.__lexical_info.add_character(previous_character, character)
                    self.__lexical_info.state = LexicalStates.BLOCK_COMMENT

                elif next_character == "/" and character == "/":
                    self.__lexical_info.state = LexicalStates.LINE_COMMENT

                elif character == "\"":
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.STRING

                elif 48 <= ord(character) <= 57:
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.NUMBER

                elif self.__lexical_structure.is_delimiter(character):
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.DELIMITER

                elif 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122:
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.IDENTIFIER

                elif self.__lexical_structure.is_relational(character, next_character):
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.RELATIONAL_OPERATOR

                elif self.__lexical_structure.is_logical(character, next_character):
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.LOGICAL_OPERATOR

                elif self.__lexical_structure.is_operator(previous_character, character, next_character):
                    if self.__lexical_structure.is_operator(previous_character, character, next_character) == 1:
                        self.__lexical_info.add_character(character)
                    elif self.__lexical_structure.is_operator(previous_character, character, next_character) == 2:
                        self.__lexical_info.add_character(previous_character, character)
                    else:
                        self.__errors_list.append(
                            self.__lexical_info.generate_token(TokenTypes.INVALID_SYMBOL)
                        )
                    self.__tokens.append(
                        self.__lexical_info.generate_token(TokenTypes.ARITHMETIC_OPERATOR)
                    )
                elif ord(character) != 10 and ord(character) != 9 and ord(character) != 32:
                    print("prev:" + previous_character + "current: "+ character + "next: " + next_character)
                    self.__lexical_info.add_character(character)
                    self.__errors_list.append(
                        self.__lexical_info.generate_token(TokenTypes.INVALID_SYMBOL)
                    )
            elif self.__lexical_info.state == LexicalStates.BLOCK_COMMENT:
                self.__block_comment_state(previous_character, str(character))
            elif self.__lexical_info.state == LexicalStates.STRING:
                self.__string_state(character)
            elif self.__lexical_info.state == LexicalStates.NUMBER:
                self.__number_state(character)
            elif self.__lexical_info.state == LexicalStates.DELIMITER:
                self.__delimiter_state(character)
            elif self.__lexical_info.state == LexicalStates.IDENTIFIER:
                self.__identifier_state(character, next_character)
            elif self.__lexical_info.state == LexicalStates.LINE_COMMENT:
                self.__line_comment_state(character)
            elif self.__lexical_info.state == LexicalStates.LOGICAL_OPERATOR:
                self.__logical_ope_state(character, next_character)
            elif self.__lexical_info.state == LexicalStates.RELATIONAL_OPERATOR:
                self.__lexical_ope_state(character, next_character)
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
