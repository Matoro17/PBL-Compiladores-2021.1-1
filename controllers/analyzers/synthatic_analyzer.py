from models.business.sythatic_node import SynthaticNode
from models.errors.synthatic_errors import SynthaticParseErrors
from models.token import Token
from util.data_structure.queue import Queue
from util.productions import EProduction
from util.synthatic.synthatic_productions import productions_functions


class SynthaticAnalyzer:

    def __init__(self):
        self.__errors = []
        self.__production_functions = productions_functions

    def start(self, queue: list[Token]) -> SynthaticNode:
        queue_list = Queue(queue)
        received: SynthaticNode = SynthaticNode(queue[0].get_lexeme())
        while queue_list.is_not_empty():
            received = self.__production_functions[EProduction.START](queue_list, self.__errors)
            if not received.is_empty():
                return received

            queue_list.remove()

        return received

    def get_errors(self) -> list[SynthaticParseErrors]:
        return self.__errors

    def clear_errors(self) -> None:
        self.__errors.clear()
