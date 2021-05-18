from models.token import Token


class SynthaticParseErrors:

    def __init__(self, production_name: str, error: list[str], lexeme: Token):
        self.__production_name = production_name
        self.error = error
        self.token = lexeme

    def __str__(self) -> str:
        if self.token:
            return "Synthatic Error on `%s`:%d:%d >> Expected one of the following tokens %s: get %s" % (
                self.__production_name,
                self.token.get_line(), self.token.get_column(), str(self.error), self.token.get_lexeme())

        return "Synthatic Error on `%s`: >> Expected one of the following tokens %s" % (
            self.__production_name, str(self.error))

    def __repr__(self) -> str:
        return self.__str__()

    def get_lexeme(self) -> Token:
        return self.token
