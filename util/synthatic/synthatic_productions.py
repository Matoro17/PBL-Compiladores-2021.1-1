from collections import Callable

from models.business.sythatic_node import SynthaticNode
from models.errors.synthatic_errors import SynthaticParseErrors
from util.data_structure.queue import Queue
from util.productions import EProduction
from util.token_types import TokenTypes

productions_functions: dict[
    EProduction, Callable[[Queue, list[SynthaticParseErrors]], SynthaticNode]
]


def sp_log_or__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Or_>\n
    Accepted productions below\n
    ['||', <Log And>, <Log Or_>]\n
    []\n
    """

    node = SynthaticNode(production="<Log Or_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['||', <Log And>, <Log Or_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "||":
        node.add(token_queue.remove())
        # Predicting for production <Log And>
        local_first_set = ["global", "local", "!", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_and(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log Or_>
        local_first_set = ["||"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_or__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_params_list(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Params List>\n
    Accepted productions below\n
    [',', <Param>, <Params List>]\n
    []\n
    """

    node = SynthaticNode(production="<Params List>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Param>, <Params List>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Param>
        local_first_set = ["boolean", "struct", "int", "string", "real"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_param(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Params List>
        local_first_set = [","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_params_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_array_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Array Decl>\n
    Accepted productions below\n
    ['[', <Array Def>, ']', <Array Vector>]\n
    """

    node = SynthaticNode(production="<Array Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['[', <Array Def>, ']', <Array Vector>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "[":
        node.add(token_queue.remove())
        # Predicting for production <Array Def>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_array_def(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "]":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["]"], token_queue.peek()))
        # Predicting for production <Array Vector>
        local_first_set = [","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_array_vector(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_param_type(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Param Type>\n
    Accepted productions below\n
    [<Type>]\n
    [id]\n
    """

    node = SynthaticNode(production="<Param Type>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Type>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in [
        "real",
        "boolean",
        "int",
        "struct",
        "string",
    ]:
        temp = sp_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [id]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())

    return node


def sp_add(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    """
    This function parse tokens for production <Add>\n
    Accepted productions below\n
    [<Mult>, <Add_>]\n
    """

    node = SynthaticNode(production="<Add>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Mult>, <Add_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "(", "!", "local", "global"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
    ):
        temp = sp_mult(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Add_>
        local_first_set = ["+", "-"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_add__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_args_list(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Args List>\n
    Accepted productions below\n
    [',', <Expr>, <Args List>]\n
    []\n
    """

    node = SynthaticNode(production="<Args List>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Expr>, <Args List>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Expr>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Args List>
        local_first_set = [","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_args_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_array_def(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Array Def>\n
    Accepted productions below\n
    [<Expr>, <Array Expr>]\n
    """

    node = SynthaticNode(production="<Array Def>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Expr>, <Array Expr>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "global", "!", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_expr(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Array Expr>
        local_first_set = [","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_array_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_var_decls(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Var Decls>\n
    Accepted productions below\n
    [<Var Decl>, <Var Decls>]\n
    []\n
    """

    node = SynthaticNode(production="<Var Decls>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Var Decl>, <Var Decls>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["typedef", "real", "struct", "string", "global", "local", "boolean", "int"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_var_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Var Decls>
        local_first_set = [
            "typedef",
            "boolean",
            "string",
            "global",
            "local",
            "int",
            "real",
            "struct",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_var_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_equate__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Equate_>\n
    Accepted productions below\n
    ['==', <Compare>, <Equate_>]\n
    ['!=', <Compare>, <Equate_>]\n
    []\n
    """

    node = SynthaticNode(production="<Equate_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['==', <Compare>, <Equate_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "==":
        node.add(token_queue.remove())
        # Predicting for production <Compare>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_compare(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Equate_>
        local_first_set = ["==", "!="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_equate__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['!=', <Compare>, <Equate_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "!=":
        node.add(token_queue.remove())
        # Predicting for production <Compare>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_compare(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Equate_>
        local_first_set = ["==", "!="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_equate__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_extends(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Extends>\n
    Accepted productions below\n
    [extends, struct, id]\n
    []\n
    """

    node = SynthaticNode(production="<Extends>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [extends, struct, id]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "extends":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "struct":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["struct"], token_queue.peek()))
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))

    # Predicting for production []
    else:
        return node

    return node


def sp_const_decls(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Const Decls>\n
    Accepted productions below\n
    [<Const Decl>, <Const Decls>]\n
    []\n
    """

    node = SynthaticNode(production="<Const Decls>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Const Decl>, <Const Decls>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["typedef", "real", "struct", "string", "global", "local", "boolean", "int"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_const_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Const Decls>
        local_first_set = [
            "typedef",
            "boolean",
            "string",
            "global",
            "local",
            "int",
            "real",
            "struct",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_const_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_value(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Value>\n
    Accepted productions below\n
    ['-', <Value>]\n
    [num]\n
    [str]\n
    [log]\n
    [local, <Access>]\n
    [global, <Access>]\n
    [id, <Id Value>]\n
    ['(', <Expr>, ')']\n
    """

    node = SynthaticNode(production="<Value>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['-', <Value>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "-":
        node.add(token_queue.remove())
        # Predicting for production <Value>
        local_first_set = ["global", "-", "(", "local"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_value(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [num]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER
    ):
        node.add(token_queue.remove())

    # Predicting for production [str]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.STRING
    ):
        node.add(token_queue.remove())

    # Predicting for production [log]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.RESERVED_WORD
    ):
        node.add(token_queue.remove())

    # Predicting for production [local, <Access>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "local":
        node.add(token_queue.remove())
        # Predicting for production <Access>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_access(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [global, <Access>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "global":
        node.add(token_queue.remove())
        # Predicting for production <Access>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_access(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [id, <Id Value>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Id Value>
        local_first_set = ["[", "("]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_id_value(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production ['(', <Expr>, ')']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "(":
        node.add(token_queue.remove())
        # Predicting for production <Expr>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))

    return node


def sp_log_unary(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Unary>\n
    Accepted productions below\n
    ['!', <Log Unary>]\n
    [<Log Value>]\n
    """

    node = SynthaticNode(production="<Log Unary>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['!', <Log Unary>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "!":
        node.add(token_queue.remove())
        # Predicting for production <Log Unary>
        local_first_set = ["global", "local", "(", "!"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [<Log Value>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["global", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_log_value(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_decls(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Decls>\n
    Accepted productions below\n
    [<Decl>, <Decls>]\n
    []\n
    """

    node = SynthaticNode(production="<Decls>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Decl>, <Decls>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in [
        "typedef",
        "function",
        "struct",
        "procedure",
    ]:
        temp = sp_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Decls>
        local_first_set = ["typedef", "struct", "function", "procedure"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_index(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Index>\n
    Accepted productions below\n
    [<Expr>]\n
    []\n
    """

    node = SynthaticNode(production="<Index>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Expr>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "global", "!", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_expr(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_and__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <And_>\n
    Accepted productions below\n
    ['&&', <Equate>, <And_>]\n
    []\n
    """

    node = SynthaticNode(production="<And_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['&&', <Equate>, <And_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "&&":
        node.add(token_queue.remove())
        # Predicting for production <Equate>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_equate(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <And_>
        local_first_set = ["&&"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_and__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_const_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Const Decl>\n
    Accepted productions below\n
    [<Type>, <Const>, <Const List>]\n
    [<Typedef>]\n
    [<Stm Scope>]\n
    [id, <Const Id>]\n
    """

    node = SynthaticNode(production="<Const Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Type>, <Const>, <Const List>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in [
        "real",
        "boolean",
        "int",
        "struct",
        "string",
    ]:
        temp = sp_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Const>
        local_first_set = []
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_const(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Const List>
        local_first_set = ["=", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_const_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [<Typedef>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["typedef"]:
        temp = sp_typedef(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Stm Scope>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["local", "global"]:
        temp = sp_stm_scope(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [id, <Const Id>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Const Id>
        local_first_set = ["(", "--", ".", "[", "++", "="]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_const_id(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    return node


def sp_accesses(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Accesses>\n
    Accepted productions below\n
    [<Access>, <Accesses>]\n
    []\n
    """

    node = SynthaticNode(production="<Accesses>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Access>, <Accesses>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["."]:
        temp = sp_access(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Accesses>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_accesses(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_param(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Param>\n
    Accepted productions below\n
    [<Param Type>, id, <Param Arrays>]\n
    """

    node = SynthaticNode(production="<Param>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Param Type>, id, <Param Arrays>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["real", "boolean", "int", "string", "struct"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_param_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))
        # Predicting for production <Param Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_param_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_var(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    """
    This function parse tokens for production <Var>\n
    Accepted productions below\n
    [id, <Arrays>]\n
    """

    node = SynthaticNode(production="<Var>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [id, <Arrays>]
    if (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_func_block(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Func Block>\n
    Accepted productions below\n
    [<Var Block>, <Func Stms>]\n
    """

    node = SynthaticNode(production="<Func Block>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Var Block>, <Func Stms>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["var"]:
        temp = sp_var_block(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Func Stms>
    local_first_set = ["read", "return", "{", "print", "global", "local", "if", "while"]
    temp_token_type = token_queue.peek().get_token_type()
    token_verification = temp_token_type == TokenTypes.IDENTIFIER
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in local_first_set
            or token_verification
    ):
        temp = sp_func_stms(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_start_block(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Start Block>\n
    Accepted productions below\n
    [start, '(', ')', '{', <Func Block>, '}']\n
    """

    node = SynthaticNode(production="<Start Block>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [start, '(', ')', '{', <Func Block>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "start":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["("], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["{"], token_queue.peek()))
        # Predicting for production <Func Block>
        local_first_set = ["var"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_func_block(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))

    return node


def sp_func_stms(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Func Stms>\n
    Accepted productions below\n
    [<Func Stm>, <Func Stms>]\n
    []\n
    """

    node = SynthaticNode(production="<Func Stms>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Func Stm>, <Func Stms>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["read", "while", "return", "{", "print", "global", "local", "if"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_func_stm(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Func Stms>
        local_first_set = [
            "read",
            "return",
            "{",
            "print",
            "global",
            "local",
            "if",
            "while",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_func_stms(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_struct_block(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Struct Block>\n
    Accepted productions below\n
    [struct, id, <Extends>, '{', <Var Decls>, '}']\n
    [typedef, struct, <Extends>, '{', <Var Decls>, '}', id, ';']\n
    """

    node = SynthaticNode(production="<Struct Block>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [struct, id, <Extends>, '{', <Var Decls>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "struct":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))
        # Predicting for production <Extends>
        local_first_set = ["extends"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_extends(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["{"], token_queue.peek()))
        # Predicting for production <Var Decls>
        local_first_set = [
            "typedef",
            "boolean",
            "string",
            "global",
            "local",
            "int",
            "real",
            "struct",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_var_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))

    # Predicting for production [typedef, struct, <Extends>, '{', <Var Decls>, '}', id, ';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "typedef":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "struct":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["struct"], token_queue.peek()))
        # Predicting for production <Extends>
        local_first_set = ["extends"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_extends(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["{"], token_queue.peek()))
        # Predicting for production <Var Decls>
        local_first_set = [
            "typedef",
            "boolean",
            "string",
            "global",
            "local",
            "int",
            "real",
            "struct",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_var_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    return node


def sp_stm_id(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Stm Id>\n
    Accepted productions below\n
    [<Assign>]\n
    [<Array>, <Arrays>, <Accesses>, <Assign>]\n
    [<Access>, <Accesses>, <Assign>]\n
    ['(', <Args>, ')', ';']\n
    """

    node = SynthaticNode(production="<Stm Id>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Assign>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["++", "--", "="]:
        temp = sp_assign(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Array>, <Arrays>, <Accesses>, <Assign>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["["]:
        temp = sp_array(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        # Predicting for production <Accesses>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_accesses(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        # Predicting for production <Assign>
        local_first_set = ["++", "--", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assign(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [<Access>, <Accesses>, <Assign>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["."]:
        temp = sp_access(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Accesses>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_accesses(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        # Predicting for production <Assign>
        local_first_set = ["++", "--", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assign(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production ['(', <Args>, ')', ';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "(":
        node.add(token_queue.remove())
        # Predicting for production <Args>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_args(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    return node


def sp_array(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Array>\n
    Accepted productions below\n
    ['[', <Index>, ']']\n
    """

    node = SynthaticNode(production="<Array>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['[', <Index>, ']']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "[":
        node.add(token_queue.remove())
        # Predicting for production <Index>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_index(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "]":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["]"], token_queue.peek()))

    return node


def sp_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Decl>\n
    Accepted productions below\n
    [<Func Decl>]\n
    [<Proc Decl>]\n
    [<Struct Block>]\n
    """

    node = SynthaticNode(production="<Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Func Decl>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["function"]:
        temp = sp_func_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Proc Decl>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["procedure"]:
        temp = sp_proc_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Struct Block>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in [
        "typedef",
        "struct",
    ]:
        temp = sp_struct_block(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_var_block(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Var Block>\n
    Accepted productions below\n
    [var, '{', <Var Decls>, '}']\n
    []\n
    """

    node = SynthaticNode(production="<Var Block>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [var, '{', <Var Decls>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "var":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["{"], token_queue.peek()))
        # Predicting for production <Var Decls>
        local_first_set = [
            "typedef",
            "boolean",
            "string",
            "global",
            "local",
            "int",
            "real",
            "struct",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_var_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))

    # Predicting for production []
    else:
        return node

    return node


def sp_array_expr(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Array Expr>\n
    Accepted productions below\n
    [',', <Array Def>]\n
    []\n
    """

    node = SynthaticNode(production="<Array Expr>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Array Def>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Array Def>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_array_def(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production []
    else:
        return node

    return node


def sp_arrays(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Arrays>\n
    Accepted productions below\n
    [<Array>, <Arrays>]\n
    []\n
    """

    node = SynthaticNode(production="<Arrays>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Array>, <Arrays>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["["]:
        temp = sp_array(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_access(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Access>\n
    Accepted productions below\n
    ['.', id, <Arrays>]\n
    """

    node = SynthaticNode(production="<Access>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['.', id, <Arrays>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ".":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))
        # Predicting for production <Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_stm_cmd(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Stm Cmd>\n
    Accepted productions below\n
    [print, '(', <Args>, ')', ';']\n
    [read, '(', <Args>, ')', ';']\n
    """

    node = SynthaticNode(production="<Stm Cmd>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [print, '(', <Args>, ')', ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "print":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["("], token_queue.peek()))
        # Predicting for production <Args>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_args(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    # Predicting for production [read, '(', <Args>, ')', ';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "read":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["("], token_queue.peek()))
        # Predicting for production <Args>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_args(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    return node


def sp_var_stm(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Var Stm>\n
    Accepted productions below\n
    [<Stm Scope>]\n
    [id, <Stm Id>]\n
    [<Stm Cmd>]\n
    """

    node = SynthaticNode(production="<Var Stm>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Stm Scope>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["local", "global"]:
        temp = sp_stm_scope(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [id, <Stm Id>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Stm Id>
        local_first_set = ["(", "--", ".", "[", "=", "++"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_stm_id(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [<Stm Cmd>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["read", "print"]:
        temp = sp_stm_cmd(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_const_block(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Const Block>\n
    Accepted productions below\n
    [const, '{', <Const Decls>, '}']\n
    []\n
    """

    node = SynthaticNode(production="<Const Block>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [const, '{', <Const Decls>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "const":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["{"], token_queue.peek()))
        # Predicting for production <Const Decls>
        local_first_set = [
            "typedef",
            "boolean",
            "string",
            "global",
            "local",
            "int",
            "real",
            "struct",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_const_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))

    # Predicting for production []
    else:
        return node

    return node


def sp_proc_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Proc Decl>\n
    Accepted productions below\n
    [procedure, id, '(', <Params>, ')', '{', <Func Block>, '}']\n
    """

    node = SynthaticNode(production="<Proc Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [procedure, id, '(', <Params>, ')', '{', <Func Block>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "procedure":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["("], token_queue.peek()))
        # Predicting for production <Params>
        local_first_set = ["boolean", "real", "int", "string", "struct"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_params(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["{"], token_queue.peek()))
        # Predicting for production <Func Block>
        local_first_set = ["var"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_func_block(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))

    return node


def sp_decl_atribute(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Decl Atribute>\n
    Accepted productions below\n
    [<Array Decl>]\n
    [<Expr>]\n
    """

    node = SynthaticNode(production="<Decl Atribute>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Array Decl>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["{"]:
        temp = sp_array_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Expr>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "global", "!", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_expr(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_compare__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Compare_>\n
    Accepted productions below\n
    ['<', <Add>, <Compare_>]\n
    ['>', <Add>, <Compare_>]\n
    ['<=', <Add>, <Compare_>]\n
    ['>=', <Add>, <Compare_>]\n
    []\n
    """

    node = SynthaticNode(production="<Compare_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['<', <Add>, <Compare_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "<":
        node.add(token_queue.remove())
        # Predicting for production <Add>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_add(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['>', <Add>, <Compare_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == ">":
        node.add(token_queue.remove())
        # Predicting for production <Add>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_add(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['<=', <Add>, <Compare_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "<=":
        node.add(token_queue.remove())
        # Predicting for production <Add>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_add(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['>=', <Add>, <Compare_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == ">=":
        node.add(token_queue.remove())
        # Predicting for production <Add>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_add(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_stm_scope(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Stm Scope>\n
    Accepted productions below\n
    [local, <Access>, <Accesses>, <Assign>]\n
    [global, <Access>, <Accesses>, <Assign>]\n
    """

    node = SynthaticNode(production="<Stm Scope>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [local, <Access>, <Accesses>, <Assign>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "local":
        node.add(token_queue.remove())
        # Predicting for production <Access>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_access(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Accesses>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_accesses(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        # Predicting for production <Assign>
        local_first_set = ["++", "--", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assign(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [global, <Access>, <Accesses>, <Assign>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "global":
        node.add(token_queue.remove())
        # Predicting for production <Access>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_access(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Accesses>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_accesses(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        # Predicting for production <Assign>
        local_first_set = ["++", "--", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assign(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    return node


def sp_func_normal_stm(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Func Normal Stm>\n
    Accepted productions below\n
    ['{', <Func Stms>, '}']\n
    [<Var Stm>]\n
    [return, <Expr>, ';']\n
    """

    node = SynthaticNode(production="<Func Normal Stm>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['{', <Func Stms>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
        node.add(token_queue.remove())
        # Predicting for production <Func Stms>
        local_first_set = [
            "read",
            "return",
            "{",
            "print",
            "global",
            "local",
            "if",
            "while",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_func_stms(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))

    # Predicting for production [<Var Stm>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["read", "local", "global", "print"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_var_stm(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [return, <Expr>, ';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "return":
        node.add(token_queue.remove())
        # Predicting for production <Expr>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    return node


def sp_else_stm(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Else Stm>\n
    Accepted productions below\n
    [else, <Func Normal Stm>]\n
    []\n
    """

    node = SynthaticNode(production="<Else Stm>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [else, <Func Normal Stm>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "else":
        node.add(token_queue.remove())
        # Predicting for production <Func Normal Stm>
        local_first_set = ["read", "local", "return", "{", "global", "print"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_func_normal_stm(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production []
    else:
        return node

    return node


def sp_log_compare(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Compare>\n
    Accepted productions below\n
    [<Log Unary>, <Log Compare_>]\n
    """

    node = SynthaticNode(production="<Log Compare>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Log Unary>, <Log Compare_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["global", "local", "(", "!"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_log_unary(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Log Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_var_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Var Decl>\n
    Accepted productions below\n
    [<Type>, <Var>, <Var List>, ';']\n
    [<Typedef>]\n
    [<Stm Scope>]\n
    [id, <Var Id>]\n
    """

    node = SynthaticNode(production="<Var Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Type>, <Var>, <Var List>, ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() in [
        "real",
        "boolean",
        "int",
        "struct",
        "string",
    ]:
        temp = sp_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Var>
        local_first_set = []
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_var(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Var List>
        local_first_set = [",", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_var_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    # Predicting for production [<Typedef>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["typedef"]:
        temp = sp_typedef(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Stm Scope>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["local", "global"]:
        temp = sp_stm_scope(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [id, <Var Id>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Var Id>
        local_first_set = ["(", "--", ".", "[", "++", "="]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_var_id(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    return node


def sp_const(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Const>\n
    Accepted productions below\n
    [id, <Arrays>]\n
    """

    node = SynthaticNode(production="<Const>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [id, <Arrays>]
    if (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_const_list(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Const List>\n
    Accepted productions below\n
    [',', <Const>, <Const List>]\n
    ['=', <Decl Atribute>, ';']\n
    """

    node = SynthaticNode(production="<Const List>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Const>, <Const List>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Const>
        local_first_set = []
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_const(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Const List>
        local_first_set = ["=", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_const_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production ['=', <Decl Atribute>, ';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "=":
        node.add(token_queue.remove())
        # Predicting for production <Decl Atribute>
        local_first_set = ["-", "{", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_decl_atribute(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    return node


def sp_var_list(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Var List>\n
    Accepted productions below\n
    [',', <Var>, <Var List>]\n
    ['=', <Expr>, <Var List>]\n
    []\n
    """

    node = SynthaticNode(production="<Var List>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Var>, <Var List>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Var>
        local_first_set = []
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_var(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Var List>
        local_first_set = [",", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_var_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['=', <Expr>, <Var List>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "=":
        node.add(token_queue.remove())
        # Predicting for production <Expr>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Var List>
        local_first_set = [",", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_var_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_array_vector(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Array Vector>\n
    Accepted productions below\n
    [',', <Array Decl>]\n
    []\n
    """

    node = SynthaticNode(production="<Array Vector>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Array Decl>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Array Decl>
        local_first_set = ["{"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_array_decl(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production []
    else:
        return node

    return node


def sp_type(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Type>\n
    Accepted productions below\n
    [int]\n
    [real]\n
    [boolean]\n
    [string]\n
    [struct, id]\n
    """

    node = SynthaticNode(production="<Type>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [int]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "int":
        node.add(token_queue.remove())

    # Predicting for production [real]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "real":
        node.add(token_queue.remove())

    # Predicting for production [boolean]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "boolean":
        node.add(token_queue.remove())

    # Predicting for production [string]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "string":
        node.add(token_queue.remove())

    # Predicting for production [struct, id]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "struct":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))

    return node


def sp_log_or(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Or>\n
    Accepted productions below\n
    [<Log And>, <Log Or_>]\n
    """

    node = SynthaticNode(production="<Log Or>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Log And>, <Log Or_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["global", "local", "!", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_log_and(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Log Or_>
        local_first_set = ["||"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_or__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_log_value(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Value>\n
    Accepted productions below\n
    [num]\n
    [str]\n
    [log]\n
    [local, <Access>]\n
    [global, <Access>]\n
    [id, <Id Value>]\n
    ['(', <Log Expr>, ')']\n
    """

    node = SynthaticNode(production="<Log Value>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [num]
    if token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER:
        node.add(token_queue.remove())

    # Predicting for production [str]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.STRING
    ):
        node.add(token_queue.remove())

    # Predicting for production [log]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.RESERVED_WORD
    ):
        node.add(token_queue.remove())

    # Predicting for production [local, <Access>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "local":
        node.add(token_queue.remove())
        # Predicting for production <Access>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_access(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [global, <Access>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "global":
        node.add(token_queue.remove())
        # Predicting for production <Access>
        local_first_set = ["."]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_access(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [id, <Id Value>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Id Value>
        local_first_set = ["[", "("]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_id_value(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production ['(', <Log Expr>, ')']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "(":
        node.add(token_queue.remove())
        # Predicting for production <Log Expr>
        local_first_set = ["global", "local", "!", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))

    return node


def sp_log_compare__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Compare_>\n
    Accepted productions below\n
    ['<', <Log Unary>, <Log Compare_>]\n
    ['>', <Log Unary>, <Log Compare_>]\n
    ['<=', <Log Unary>, <Log Compare_>]\n
    ['>=', <Log Unary>, <Log Compare_>]\n
    []\n
    """

    node = SynthaticNode(production="<Log Compare_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['<', <Log Unary>, <Log Compare_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "<":
        node.add(token_queue.remove())
        # Predicting for production <Log Unary>
        local_first_set = ["global", "local", "(", "!"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['>', <Log Unary>, <Log Compare_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == ">":
        node.add(token_queue.remove())
        # Predicting for production <Log Unary>
        local_first_set = ["global", "local", "(", "!"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['<=', <Log Unary>, <Log Compare_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "<=":
        node.add(token_queue.remove())
        # Predicting for production <Log Unary>
        local_first_set = ["global", "local", "(", "!"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['>=', <Log Unary>, <Log Compare_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == ">=":
        node.add(token_queue.remove())
        # Predicting for production <Log Unary>
        local_first_set = ["global", "local", "(", "!"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_assign(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assign>\n
    Accepted productions below\n
    ['=', <Expr>, ';']\n
    ['++', ';']\n
    ['--', ';']\n
    """

    node = SynthaticNode(production="<Assign>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['=', <Expr>, ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
        node.add(token_queue.remove())
        # Predicting for production <Expr>
        local_first_set = ["-", "global", "!", "local", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    # Predicting for production ['++', ';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "++":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    # Predicting for production ['--', ';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "--":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    return node


def sp_log_equate(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Equate>\n
    Accepted productions below\n
    [<Log Compare>, <Log Equate_>]\n
    """

    node = SynthaticNode(production="<Log Equate>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Log Compare>, <Log Equate_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["global", "local", "!", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_log_compare(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Log Equate_>
        local_first_set = ["==", "!="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_equate__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_args(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Args>\n
    Accepted productions below\n
    [<Expr>, <Args List>]\n
    []\n
    """

    node = SynthaticNode(production="<Args>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Expr>, <Args List>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "global", "!", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_expr(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Args List>
        local_first_set = [","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_args_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_log_and__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log And_>\n
    Accepted productions below\n
    ['&&', <Log Equate>, <Log And_>]\n
    []\n
    """

    node = SynthaticNode(production="<Log And_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['&&', <Log Equate>, <Log And_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "&&":
        node.add(token_queue.remove())
        # Predicting for production <Log Equate>
        local_first_set = ["global", "local", "(", "!"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_equate(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log And_>
        local_first_set = ["&&"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_and__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_or(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    """
    This function parse tokens for production <Or>\n
    Accepted productions below\n
    [<And>, <Or_>]\n
    """

    node = SynthaticNode(production="<Or>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<And>, <Or_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "(", "!", "local", "global"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
    ):
        temp = sp_and(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Or_>
        local_first_set = ["||"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_or__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_id_value(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Id Value>\n
    Accepted productions below\n
    [<Arrays>, <Accesses>]\n
    ['(', <Args>, ')']\n
    """

    node = SynthaticNode(production="<Id Value>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Arrays>, <Accesses>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["["]:
        temp = sp_arrays(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Accesses>
    local_first_set = ["."]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_accesses(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production ['(', <Args>, ')']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "(":
        node.add(token_queue.remove())
        # Predicting for production <Args>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_args(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))

    return node


def sp_or__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Or_>\n
    Accepted productions below\n
    ['||', <And>, <Or_>]\n
    []\n
    """

    node = SynthaticNode(production="<Or_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['||', <And>, <Or_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "||":
        node.add(token_queue.remove())
        # Predicting for production <And>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_and(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Or_>
        local_first_set = ["||"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_or__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_log_and(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log And>\n
    Accepted productions below\n
    [<Log Equate>, <Log And_>]\n
    """

    node = SynthaticNode(production="<Log And>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Log Equate>, <Log And_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["global", "local", "(", "!"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_log_equate(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Log And_>
        local_first_set = ["&&"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_and__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_func_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Func Decl>\n
    Accepted productions below\n
    [function, <Param Type>, id, '(', <Params>, ')', '{', <Func Block>, '}']\n
    """

    node = SynthaticNode(production="<Func Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [function, <Param Type>, id, '(', <Params>, ')', '{', <Func Block>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "function":
        node.add(token_queue.remove())
        # Predicting for production <Param Type>
        local_first_set = ["real", "boolean", "int", "string", "struct"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_param_type(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["("], token_queue.peek()))
        # Predicting for production <Params>
        local_first_set = ["boolean", "real", "int", "string", "struct"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_params(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["{"], token_queue.peek()))
        # Predicting for production <Func Block>
        local_first_set = ["var"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_func_block(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["}"], token_queue.peek()))

    return node


def sp_param_arrays(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Param Arrays>\n
    Accepted productions below\n
    ['[', ']', <Param Mult Arrays>]\n
    []\n
    """

    node = SynthaticNode(production="<Param Arrays>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['[', ']', <Param Mult Arrays>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "[":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "]":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["]"], token_queue.peek()))
        # Predicting for production <Param Mult Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_param_mult_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_param_mult_arrays(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Param Mult Arrays>\n
    Accepted productions below\n
    ['[', num, ']', <Param Mult Arrays>]\n
    []\n
    """

    node = SynthaticNode(production="<Param Mult Arrays>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['[', num, ']', <Param Mult Arrays>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "[":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.NUMBER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["num"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "]":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["]"], token_queue.peek()))
        # Predicting for production <Param Mult Arrays>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_param_mult_arrays(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_unary(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Unary>\n
    Accepted productions below\n
    ['!', <Unary>]\n
    [<Value>]\n
    """

    node = SynthaticNode(production="<Unary>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['!', <Unary>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "!":
        node.add(token_queue.remove())
        # Predicting for production <Unary>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [<Value>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["global", "-", "(", "local"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_value(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_typedef(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Typedef>\n
    Accepted productions below\n
    [typedef, <Type>, id, ';']\n
    """

    node = SynthaticNode(production="<Typedef>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [typedef, <Type>, id, ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "typedef":
        node.add(token_queue.remove())
        # Predicting for production <Type>
        local_first_set = ["real", "boolean", "int", "struct", "string"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_type(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["id"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    return node


def sp_var_id(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Var Id>\n
    Accepted productions below\n
    [<Var>, <Var List>, ';']\n
    [<Stm Id>]\n
    """

    node = SynthaticNode(production="<Var Id>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Var>, <Var List>, ';']
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in []
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_var(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Var List>
        local_first_set = [",", "="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_var_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    # Predicting for production [<Stm Id>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in [
        "(",
        "--",
        ".",
        "[",
        "=",
        "++",
    ]:
        temp = sp_stm_id(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_mult__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Mult_>\n
    Accepted productions below\n
    ['*', <Unary>, <Mult_>]\n
    ['/', <Unary>, <Mult_>]\n
    []\n
    """

    node = SynthaticNode(production="<Mult_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['*', <Unary>, <Mult_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "*":
        node.add(token_queue.remove())
        # Predicting for production <Unary>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Mult_>
        local_first_set = ["*", "/"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_mult__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['/', <Unary>, <Mult_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "/":
        node.add(token_queue.remove())
        # Predicting for production <Unary>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_unary(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Mult_>
        local_first_set = ["*", "/"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_mult__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_expr(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Expr>\n
    Accepted productions below\n
    [<Or>]\n
    """

    node = SynthaticNode(production="<Expr>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Or>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "global", "!", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
    ):
        temp = sp_or(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_params(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Params>\n
    Accepted productions below\n
    [<Param>, <Params List>]\n
    []\n
    """

    node = SynthaticNode(production="<Params>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Param>, <Params List>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["boolean", "struct", "int", "string", "real"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_param(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Params List>
        local_first_set = [","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_params_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_and(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    """
    This function parse tokens for production <And>\n
    Accepted productions below\n
    [<Equate>, <And_>]\n
    """

    node = SynthaticNode(production="<And>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Equate>, <And_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "(", "!", "local", "global"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_equate(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <And_>
        local_first_set = ["&&"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_and__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_const_id(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Const Id>\n
    Accepted productions below\n
    [<Const>, <Const List>, ';']\n
    [<Stm Id>]\n
    """

    node = SynthaticNode(production="<Const Id>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Const>, <Const List>, ';']
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in []
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_const(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Const List>
        local_first_set = ["=", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_const_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([";"], token_queue.peek()))

    # Predicting for production [<Stm Id>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in [
        "(",
        "--",
        ".",
        "[",
        "=",
        "++",
    ]:
        temp = sp_stm_id(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_add__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Add_>\n
    Accepted productions below\n
    ['+', <Mult>, <Add_>]\n
    ['-', <Mult>, <Add_>]\n
    []\n
    """

    node = SynthaticNode(production="<Add_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['+', <Mult>, <Add_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "+":
        node.add(token_queue.remove())
        # Predicting for production <Mult>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_mult(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Add_>
        local_first_set = ["+", "-"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_add__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['-', <Mult>, <Add_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "-":
        node.add(token_queue.remove())
        # Predicting for production <Mult>
        local_first_set = ["-", "(", "!", "local", "global"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_mult(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Add_>
        local_first_set = ["+", "-"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_add__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_func_stm(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Func Stm>\n
    Accepted productions below\n
    [if, '(', <Log Expr>, ')', then, <Func Normal Stm>, <Else Stm>]\n
    [while, '(', <Log Expr>, ')', <Func Stm>]\n
    [<Func Normal Stm>]\n
    """

    node = SynthaticNode(production="<Func Stm>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [if, '(', <Log Expr>, ')', then, <Func Normal Stm>, <Else Stm>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "if":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["("], token_queue.peek()))
        # Predicting for production <Log Expr>
        local_first_set = ["global", "local", "!", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == "then":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["then"], token_queue.peek()))
        # Predicting for production <Func Normal Stm>
        local_first_set = ["read", "local", "return", "{", "global", "print"]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_func_normal_stm(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Else Stm>
        local_first_set = ["else"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_else_stm(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production [while, '(', <Log Expr>, ')', <Func Stm>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "while":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors(["("], token_queue.peek()))
        # Predicting for production <Log Expr>
        local_first_set = ["global", "local", "!", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_expr(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors([")"], token_queue.peek()))
        # Predicting for production <Func Stm>
        local_first_set = [
            "read",
            "while",
            "return",
            "{",
            "print",
            "global",
            "local",
            "if",
        ]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_func_stm(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))

    # Predicting for production [<Func Normal Stm>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["read", "local", "return", "{", "global", "print"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_func_normal_stm(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_compare(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Compare>\n
    Accepted productions below\n
    [<Add>, <Compare_>]\n
    """

    node = SynthaticNode(production="<Compare>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Add>, <Compare_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "global", "!", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
    ):
        temp = sp_add(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Compare_>
        local_first_set = ["<=", "<", ">=", ">"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_compare__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_equate(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Equate>\n
    Accepted productions below\n
    [<Compare>, <Equate_>]\n
    """

    node = SynthaticNode(production="<Equate>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Compare>, <Equate_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "global", "!", "local", "("]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_compare(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Equate_>
        local_first_set = ["==", "!="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_equate__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_log_equate__(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Equate_>\n
    Accepted productions below\n
    ['==', <Log Compare>, <Log Equate_>]\n
    ['!=', <Log Compare>, <Log Equate_>]\n
    []\n
    """

    node = SynthaticNode(production="<Log Equate_>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['==', <Log Compare>, <Log Equate_>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "==":
        node.add(token_queue.remove())
        # Predicting for production <Log Compare>
        local_first_set = ["global", "local", "!", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_compare(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log Equate_>
        local_first_set = ["==", "!="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_equate__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production ['!=', <Log Compare>, <Log Equate_>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "!=":
        node.add(token_queue.remove())
        # Predicting for production <Log Compare>
        local_first_set = ["global", "local", "!", "("]
        temp_token_type = token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.RESERVED_WORD
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_log_compare(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
        # Predicting for production <Log Equate_>
        local_first_set = ["==", "!="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_log_equate__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_mult(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Mult>\n
    Accepted productions below\n
    [<Unary>, <Mult_>]\n
    """

    node = SynthaticNode(production="<Mult>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Unary>, <Mult_>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["-", "(", "!", "local", "global"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_unary(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Mult_>
        local_first_set = ["*", "/"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_mult__(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_program(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Program>\n
    Accepted productions below\n
    [<Const Block>, <Var Block>, <Decls>, <Start Block>, <Decls>]\n
    """

    node = SynthaticNode(production="<Program>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Const Block>, <Var Block>, <Decls>, <Start Block>, <Decls>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["const"]:
        temp = sp_const_block(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Var Block>
    local_first_set = ["var"]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_var_block(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Decls>
    local_first_set = ["typedef", "struct", "function", "procedure"]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_decls(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Start Block>
    local_first_set = ["start"]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_start_block(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        else:
            error_list.append(SynthaticParseErrors(local_first_set, token_queue.peek()))
    # Predicting for production <Decls>
    local_first_set = ["typedef", "struct", "function", "procedure"]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_decls(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_log_expr(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Log Expr>\n
    Accepted productions below\n
    [<Log Or>]\n
    """

    node = SynthaticNode(production="<Log Expr>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Log Or>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["global", "local", "(", "!"]
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.RESERVED_WORD
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_log_or(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


productions_functions = {
    EProduction.START: sp_program
}
