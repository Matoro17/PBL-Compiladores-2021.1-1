from collections import Callable

from models.business.sythatic_node import SynthaticNode
from models.errors.synthatic_errors import SynthaticParseErrors
from util.data_structure.queue import Queue
from util.productions import EProduction

productions_functions: dict[EProduction, Callable[[Queue, list[SynthaticParseErrors]], SynthaticNode]]


def sp_start(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_proc_decl(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_param(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_assignment_matrix_aux1(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_value_assigned_vector(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_body_item(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_formal_parameter_list_read(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_prefixgloballocal(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_function_call(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_body_item_procedure(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_body(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_relational(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_conditional_expression(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_while(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_number(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_base(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_assignment_matrix_aux2(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_vector(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_index(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_value_assigned_matrix(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_matrix(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_struct_decl(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_conditional_operator(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_formal_parameter_list(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_variable(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_then_procedure(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_constlist(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_function_declaration(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_const(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_read(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_dimensao_matrix2(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_relational_expression(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_delimiter_var(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_global_decl(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_assign(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_variableslist(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_logical_expression(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_value(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_exp(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_expression_value(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_type(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_mult_exp(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_delimiter_const(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_term(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_add_exp(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_if(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_expression_value_logical(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_extends(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_assignment_vector(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_else(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_logical_denied(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_body_procedure(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_return_statement(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_params(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_while_procedure(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_if_procedure(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_aux(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_program(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_logical(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_const_decl(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_then(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_decls(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_assignment_vector_aux2(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_typedef_decl(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_decl(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_print(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_assignment_matrix(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_var_decl(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_boolean_literal(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_assignment_vector_aux1(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


def sp_else_procedure(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    pass


productions_functions = {
    EProduction.START: sp_start
}
