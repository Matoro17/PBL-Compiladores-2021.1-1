from enum import Enum


class TokenTypes(Enum):
    # Types used in output file
    RESERVED_WORD = "PRE"
    IDENTIFIER = "IDE"
    NUMBER = "NRO"
    DELIMITER = "DEL"
    RELATIONAL_OPERATOR = "REL"
    LOGIC_OPERATOR = "LOG"
    ARITHMETIC_OPERATOR = "ART"
    INVALID_SYMBOL = "SIB"
    MALFORMED_CHAIN = "CMF"
    MALFORMED_NUMBER = "NMF"
    MALFORMED_COMMENT = "CoMF"
    MALFORMED_OPERATOR = "OpMF"
    STRING = "CAD"
    # Types for internal use
    BLOCK_COMMENT = "BLC"
    LINE_COMMENT = "LNC"
