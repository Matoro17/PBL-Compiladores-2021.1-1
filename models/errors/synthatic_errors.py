from models.token import Token


class SynthaticParseErrors:

    def __init__(self, error: list[str], lexeme: Token):
        self.error = error
        self.token = lexeme

    def __str__(self) -> str:
        if self.token:
            return "Synthatic Error:" + str(self.token.get_line()) + ":" + str(
                self.token.get_column()) + " >> Expected one of the following tokens " + str(self.error) + ": get " \
                   + self.token.get_lexeme()

        return "Synthatic Error:" + " >> Expected one of the following tokens " + str(self.error)

    def __repr__(self) -> str:
        return self.__str__()

    def get_lexeme(self) -> Token:
        return self.token
