from models.business.grammar_info import FirstFollow
from models.business.sythatic_node import SynthaticNode
from models.errors.synthatic_errors import SynthaticParseErrors
from models.token import Token, TokenTypes


class SynthaticAnalyzer:

    def __init__(self):
        self.__productions = FirstFollow().get_productions()
        self.__errors = []

    @staticmethod
    def is_production(name: str) -> bool:
        return name.find("<.*>") > 0

    def __is_synchronization_token(self, token: Token, derivation: str) -> bool:
        return self.follow.get(derivation.replaceAll("[<|>]", "")).contains(
            token.getLexeme().getValue()) or TokenTypes.getInstance().delimiters().contains(
            token.getLexeme().getValue())

    def __is_last_empty(synthaticNode: SynthaticNode) -> bool:
        return synthaticNode.is_empty()

    def __automatic(self, production: str, queue: list[Token]) -> SynthaticNode:
        if (queue.peek() == None):
            if (production.equals(FirstFollow.getInstance().StartSymbol)):
                return SynthaticNode()

            return None

        index = 0
        for produces in self.productions.get(production):
            hasConsumed = SynthaticNode(production)
            count = 0
            for derivation in produces:
                if self.is_production(derivation):
                    hasError = False
                    if self.predict(derivation.replaceAll("[<|>]", ""), queue.peek()):
                        synthaticNode = self.__automatic(derivation, queue)
                        if synthaticNode != None:
                            if self.__is_last_empty(synthaticNode) and index < self.productions.get(
                                    production).size() - 1:
                                count += 1
                                continue

                            hasConsumed.add(synthaticNode)
                        elif not self.first.get(derivation.replaceAll("[<|>]", "")).contains(""):
                            hasError = True

                    elif count >= 1:
                        hasError = True
                        consume = queue.peek()
                        while consume != None and not self.isSynchronizationToken(consume, derivation):
                            queue.remove()
                            consume = queue.peek()
                            self.errors.add(SynthaticParseErrors(self.first.get(production.replaceAll("[<|>]", "")),
                                                                 consume != None and consume.get_lexeme() or None))

                            if queue.peek() != None:
                                consume = queue.remove()
                                self.errors.add(SynthaticParseErrors(self.first.get(production.replaceAll("[<|>]", "")),
                                                                     consume != None and consume.getLexeme() or None))

                            if hasError:
                                token = queue.peek()
                                lexeme = token != None and token.get_lexeme() or None
                                self.errors.add(
                                    SynthaticParseErrors(self.first.get(derivation.replaceAll("[<|>]", "")), lexeme))

                        else:
                            token = queue.peek()
                            if token != None:
                                if (token.get_lexeme().getValue().equals(derivation.replace("\'", ""))):
                                    hasConsumed.add(SynthaticNode(queue.remove(), derivation))
                                elif self.predict(derivation.replace("\'", ""), token):
                                    hasConsumed.add(SynthaticNode(queue.remove(), derivation))
                                elif "".equals(derivation):
                                    hasConsumed.add(SynthaticNode())
                                    count += 1
                                    continue
                                elif count > 0:
                                    if count == 1 and self.first.get(production.replaceAll("[<|>]", "")).contains(""):
                                        break
                                    else:
                                        self.errors.add(
                                            SynthaticParseErrors(self.first.get(production.replaceAll("[<|>]", "")),
                                                                 token.get_lexeme()))
                                        return None

                        count += 1
                        if hasConsumed.is_empty():
                            break

                    if not hasConsumed.is_empty() and count != produces.size():
                        return None
                    elif not hasConsumed.is_empty():
                        return hasConsumed

                    index += 1

                return None

    def start(self, queue: list[Token]) -> SynthaticNode:
        while len(queue) > 0:
            received = self.__automatic(FirstFollow().StartSymbol, queue)
            if received:
                return received

            queue.remove()

        return None

    def get_errors(self) -> list[SynthaticParseErrors]:
        return self.errors

    def clear_errors(self) -> None:
        self.__errors = []
