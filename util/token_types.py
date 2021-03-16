from enum import Enum


class TokenTypes(Enum):
    # Types used in output file
    RESERVED_WORD = "PRE"
    IDENTIFIER = "IDE"
    NUMBER = "NRO"
    DELIMITER = "DEL"
    RELATIONAL_OPERATOR = "REL"
    LOGICAL_OPERATOR = "LOG"
    ARITHMETIC_OPERATOR = "ART"
    STRING = "CAD"
    # Types for internal use
    BLOCK_COMMENT = "BLC"
    LINE_COMMENT = "LNC"
    # Errors
    INVALID_SYMBOL = "SIB"
    MALFORMED_STRING = "CMF"
    MALFORMED_NUMBER = "NMF"
    MALFORMED_COMMENT = "CoMF"
    MALFORMED_OPERATOR = "OpMF"
