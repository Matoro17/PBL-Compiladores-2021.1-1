from collections.abc import Callable
from typing import BinaryIO

import util.lexycal.lexical_validators as validators
from controllers.analyzers.synthatic_analyzer import SynthaticAnalyzer
from models.lexical_information import LexicalInformation
from models.token import Token
from util.helpers.string_helpers import input_to_output
from util.lexycal.lexical_states import LexicalStates
from util.lexycal.lexical_structure import LexicalStructure
from util.token_types import TokenTypes


class LexicalAnalyzer:
    def __init__(self):
        self.__lexical_info = LexicalInformation()
        self.__lexical_structure = LexicalStructure()
        self.__tokens = []
        self.__errors_list = []
        self.__filename = ""

    def _store_token(self, token_type: TokenTypes, is_error=False) -> Token:
        new_token = self.__lexical_info.generate_token(token_type)
        if new_token.get_lexeme().strip() != "":
            if is_error:
                self.__errors_list.append(new_token)
            else:
                self.__tokens.append(new_token)
        return new_token

    def get_errors(self) -> list[str]:
        return self.__errors_list

    def __block_comment_state(self, previous_character: str, character: str) -> None:
        self.__lexical_info.add_character(character)
        if character == "/" and previous_character == "*":
            self.__lexical_info.state = LexicalStates.NIL
            self._store_token(TokenTypes.BLOCK_COMMENT)

    def __line_comment_state(self, character) -> None:
        if character == "\n":
            self.__lexical_info.state = LexicalStates.NIL
            self._store_token(TokenTypes.LINE_COMMENT)
        else:
            self.__lexical_info.add_character(character)

    def __string_state(self, previous_character: str, character: str) -> None:
        self.__lexical_info.add_character(character)
        # TODO Still needs to fix problems like "hello \\"
        if (
                previous_character != "\\"
                and character == self.__lexical_info.get_first_character()
        ):
            self.__lexical_info.state = LexicalStates.NIL
            self._store_token(TokenTypes.STRING)

    def __number_state(self, character: str, next_character: str) -> None:
        self.__lexical_info.add_character(character)
        lexeme = self.__lexical_info.get_lexeme()
        # TODO verify if next_character is a a invalid symbol
        if character.isnumeric():
            if next_character != "." and not next_character.isnumeric():
                if (
                        self.__lexical_structure.is_end_lexeme(next_character)
                        or next_character.isspace()
                ):
                    self.__lexical_info.state = LexicalStates.NIL
                    if validators.is_valid_number(lexeme):
                        self._store_token(TokenTypes.NUMBER)
                    else:
                        self._store_token(TokenTypes.MALFORMED_NUMBER, True)
        elif character != "." or next_character.isspace():
            self.__lexical_info.state = LexicalStates.NIL
            self._store_token(TokenTypes.MALFORMED_NUMBER, True)
        elif character == "." and self.__lexical_structure.is_end_lexeme(next_character):
            self.__lexical_info.state = LexicalStates.NIL
            if validators.is_valid_number(lexeme):
                self._store_token(TokenTypes.NUMBER)
            else:
                self._store_token(TokenTypes.MALFORMED_NUMBER, True)

    @staticmethod
    def __is_character_identifier(character) -> bool:
        return (
                ord("0") <= ord(character) <= ord("9")
                or ord(character) == ord("_")
                or ord("A") <= ord(character) <= ord("Z")
                or ord("a") <= ord(character) <= ord("z")
        )

    def __identifier_state(self, character: str, next_character: str) -> None:
        if self.__is_character_identifier(character):
            self.__lexical_info.add_character(character)
        else:
            self.__lexical_info.add_character(character)
            self._store_token(TokenTypes.INVALID_SYMBOL, True)

        if self.__lexical_structure.is_end_lexeme(next_character):
            self.__lexical_info.state = LexicalStates.NIL
            if self.__lexical_structure.is_reserved(self.__lexical_info.get_lexeme()):
                self._store_token(TokenTypes.RESERVED_WORD)
            else:
                self._store_token(TokenTypes.IDENTIFIER)

    def __operator_state(
            self,
            callback: Callable[[str, str], [bool, bool]],
            token_type: TokenTypes,
            character: str,
            previous_character: str,
    ) -> None:
        valid_operator = callback(previous_character, character)
        if valid_operator[1]:
            self.__lexical_info.add_character(character)
            self._store_token(token_type)
        else:
            self._store_token(token_type)
            self.__lexical_info.add_character(character)
        self.__lexical_info.state = LexicalStates.NIL

    def __arithmetic_op_state(self, character: str, previous_character: str) -> None:
        self.__operator_state(
            self.__lexical_structure.is_arithmetic,
            TokenTypes.ARITHMETIC_OPERATOR,
            character,
            previous_character,
        )

    def __logical_op_state(self, character: str, previous_character: str) -> None:
        self.__operator_state(
            self.__lexical_structure.is_logical,
            TokenTypes.LOGICAL_OPERATOR,
            character,
            previous_character,
        )

    def __relational_op_state(self, character: str, previous_character: str) -> None:
        self.__operator_state(
            self.__lexical_structure.is_relational,
            TokenTypes.RELATIONAL_OPERATOR,
            character,
            previous_character,
        )

    def __parse_line(self, line_data: bytes) -> None:
        previous_character = ""
        for column in range(0, len(line_data)):
            self.__lexical_info.column = column + 1
            character = str(line_data[column])

            # look ahead variable
            next_character = ""
            if column + 1 < len(line_data):
                next_character = line_data[column + 1]

            # Relational return
            relational_type = self.__lexical_structure.is_relational(
                character, next_character
            )
            logical_type = self.__lexical_structure.is_logical(
                character, next_character
            )
            arithmetic_type = self.__lexical_structure.is_arithmetic(
                character, next_character
            )

            if self.__lexical_info.state == LexicalStates.NIL:
                # Start point, verify first character in lexeme

                # Top Priorities states
                if character == "/" and next_character == "*":
                    self.__lexical_info.add_character(previous_character, character)
                    self.__lexical_info.state = LexicalStates.BLOCK_COMMENT

                elif next_character == "/" and character == "/":
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.LINE_COMMENT

                elif character == '"' or character == "'":
                    self.__lexical_info.add_character(character)
                    self.__lexical_info.state = LexicalStates.STRING

                # Common States
                elif ord("0") <= ord(character) <= ord("9") or (character == "-" and next_character.isdigit()):
                    self.__lexical_info.add_character(character)
                    if self.__lexical_structure.is_end_lexeme(next_character) and next_character != ".":
                        self._store_token(TokenTypes.NUMBER)
                    else:
                        self.__lexical_info.state = LexicalStates.NUMBER

                elif ord("A") <= ord(character) <= ord("Z") or ord("a") <= ord(character) <= ord("z"):
                    self.__lexical_info.add_character(character)
                    if self.__lexical_structure.is_end_lexeme(next_character):
                        self._store_token(TokenTypes.IDENTIFIER)
                    else:
                        self.__lexical_info.state = LexicalStates.IDENTIFIER

                elif relational_type[0]:
                    self.__lexical_info.add_character(character)
                    if relational_type[1]:
                        self.__lexical_info.state = LexicalStates.RELATIONAL_OPERATOR
                    else:
                        self._store_token(TokenTypes.RELATIONAL_OPERATOR)

                elif logical_type[0]:
                    self.__lexical_info.add_character(character)
                    if logical_type[1]:
                        self.__lexical_info.state = LexicalStates.LOGICAL_OPERATOR
                    else:
                        self._store_token(TokenTypes.LOGICAL_OPERATOR)

                elif arithmetic_type[0]:
                    self.__lexical_info.add_character(character)
                    if arithmetic_type[1]:
                        self.__lexical_info.state = LexicalStates.ARITHMETIC_OPERATOR
                    else:
                        self._store_token(TokenTypes.ARITHMETIC_OPERATOR)

                elif self.__lexical_structure.is_delimiter(character):
                    self.__lexical_info.add_character(character)
                    self._store_token(TokenTypes.DELIMITER)

                elif (
                        ord(character) != 10
                        and ord(character) != 9
                        and ord(character) != 32
                ):
                    self.__lexical_info.add_character(character)
                    self._store_token(TokenTypes.INVALID_SYMBOL, True)

            # Here start all other states
            elif self.__lexical_info.state == LexicalStates.BLOCK_COMMENT:
                self.__block_comment_state(previous_character, str(character))
            elif self.__lexical_info.state == LexicalStates.STRING:
                self.__string_state(previous_character, character)
            elif self.__lexical_info.state == LexicalStates.NUMBER:
                self.__number_state(character, next_character)
            elif self.__lexical_info.state == LexicalStates.IDENTIFIER:
                self.__identifier_state(character, next_character)
            elif self.__lexical_info.state == LexicalStates.LINE_COMMENT:
                self.__line_comment_state(character)
            elif self.__lexical_info.state == LexicalStates.LOGICAL_OPERATOR:
                self.__logical_op_state(character, previous_character)
            elif self.__lexical_info.state == LexicalStates.RELATIONAL_OPERATOR:
                self.__relational_op_state(character, previous_character)
            elif self.__lexical_info.state == LexicalStates.ARITHMETIC_OPERATOR:
                self.__arithmetic_op_state(character, previous_character)
            column += 1
            previous_character = character

        if self.__lexical_info.state == LexicalStates.IDENTIFIER:
            self._store_token(TokenTypes.IDENTIFIER)
        elif self.__lexical_info.state == LexicalStates.NUMBER:
            self._store_token(TokenTypes.NUMBER)
        if self.__lexical_info.state != LexicalStates.NIL:
            if self.__lexical_info.state == LexicalStates.STRING:
                self._store_token(TokenTypes.MALFORMED_STRING, True)
            if self.__lexical_info.state != LexicalStates.BLOCK_COMMENT:
                self._store_token(TokenTypes.MALFORMED_COMMENT, True)

    def start(self, file_pointer: BinaryIO) -> None:
        line_number = 0
        for current_line in file_pointer.readlines():
            self.__lexical_info.line_number = line_number + 1
            self.__parse_line(current_line)
            line_number += 1
        if self.__lexical_info.state == LexicalStates.BLOCK_COMMENT:
            self._store_token(TokenTypes.MALFORMED_COMMENT, True)

        if not self.__errors_list:
            print("Lexical: Success! No lexical errors")
        else:
            print("Lexical: Finished! With lexical errors")

        file_pointer = open(input_to_output(self.__filename), 'w')

        file_pointer.write("".join(str(v) for v in self.__tokens))
        file_pointer.write("\n")
        file_pointer.write("".join(str(v) for v in self.__errors_list))

        temp_synthatic = SynthaticAnalyzer()
        temp_synthatic.start(self.__tokens)
        if not temp_synthatic.get_errors():
            print("Synthatic: Success! No Synthatic errors")
        else:
            print("Synthatic: Finished! With Synthatic errors")
        file_pointer.write("\n".join(str(v) for v in temp_synthatic.get_errors()))
        file_pointer.write("\n")
        self.__tokens.clear()
        self.__errors_list.clear()

    def set_filename(self, filename: str) -> None:
        self.__filename = filename
