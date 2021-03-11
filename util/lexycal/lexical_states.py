from enum import Enum


class LexicalStates(Enum):
    NIL = 0
    LINE_COMMENT = 1
    BLOCK_COMMENT = 2
    STRING = 3
    IDENTIFIER = 4
    NUMBER = 5
    LOGICAL_OPERATOR = 6
    RELATIONAL_OPERATOR = 7
    DELIMITER = 8
