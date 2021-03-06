from models.token import Token


class SynthaticNode:

    def __init__(self, production: str, token: Token = None):
        self.nodeList = []
        self.token: Token = token
        self.empty: bool = token is None
        self.production: str = production

    def add(self, synthatic_node) -> None:
        if not synthatic_node:
            if self.empty:
                self.empty = False

            self.nodeList.append(synthatic_node)

    def get_token(self) -> Token:
        return self.token

    def get_node_list(self) -> list:
        return self.nodeList

    def is_empty(self) -> bool:
        return self.empty

    def is_not_empty(self) -> bool:
        return not self.empty

    def get_production(self) -> str:
        return self.production

    def __str__(self):
        return "SynthaticNode{" + str(self.nodeList) + ", " + self.production + '}'
