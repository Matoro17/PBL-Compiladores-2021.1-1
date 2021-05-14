from models.business.sythatic_node import SynthaticNode
from models.errors.synthatic_errors import SynthaticParseErrors
from util.data_structure.queue import Queue
from util.productions import EProduction


def sp_start(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


productions_functions = {
    EProduction.START: sp_start
}
