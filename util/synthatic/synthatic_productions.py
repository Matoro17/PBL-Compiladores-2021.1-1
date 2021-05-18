from collections import Callable

from models.business.sythatic_node import SynthaticNode
from models.errors.synthatic_errors import SynthaticParseErrors
from util.data_structure.queue import Queue
from util.productions import EProduction
from util.token_types import TokenTypes

productions_functions: dict[
    EProduction, Callable[[Queue, list[SynthaticParseErrors]], SynthaticNode]
]


def sp_base(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Base>\n
    Accepted productions below\n
    [<Type>]\n
    [struct, <Extends>, '{', <VariablesList>, '}']\n
    [<Struct Decl>]\n
    """

    node = SynthaticNode(production="<Base>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Type>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["boolean", "int", "struct", "string", "real"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [struct, <Extends>, '{', <VariablesList>, '}']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "struct":
        node.add(token_queue.remove())
        # Predicting for production <Extends>
        local_first_set = ["extends"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_extends(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Base>", ["{"], token_queue.peek()))
        # Predicting for production <VariablesList>
        local_first_set = ["boolean", "int", "struct", "real", "string"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_variables_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Base>", ["}"], token_queue.peek()))

    # Predicting for production [<Struct Decl>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["struct"]:
        temp = sp_struct_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_relational_expression(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Relational Expression>\n
    Accepted productions below\n
    [<Exp>, <Relational>]\n
    """

    node = SynthaticNode(production="<Relational Expression>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Exp>, <Relational>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "local", "global", "-", "false"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_exp(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Relational>
        local_first_set = [">", "<", "==", ">=", "!=", "<="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_relational(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Relational Expression>", local_first_set, token_queue.peek()
                )
            )

    return node


def sp_formal_parameter_list_read(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Formal Parameter List Read>\n
    Accepted productions below\n
    [Identifier]\n
    [<Formal Parameter List Read>, ',', Identifier]\n
    """

    node = SynthaticNode(production="<Formal Parameter List Read>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [Identifier]
    if (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())

    # Predicting for production [<Formal Parameter List Read>, ',', Identifier]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in []
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_formal_parameter_list_read(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Formal Parameter List Read>", [","], token_queue.peek()
                )
            )
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Formal Parameter List Read>", ["Identifier"], token_queue.peek()
                )
            )

    return node


def sp_conditional_operator(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Conditional Operator>\n
    Accepted productions below\n
    ['&&']\n
    ['||']\n
    """

    node = SynthaticNode(production="<Conditional Operator>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['&&']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "&&":
        node.add(token_queue.remove())

    # Predicting for production ['||']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "||":
        node.add(token_queue.remove())

    return node


def sp_params(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Params>\n
    Accepted productions below\n
    [<Param>, ',', <Params>]\n
    [<Param>]\n
    []\n
    """

    node = SynthaticNode(production="<Params>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Param>, ',', <Params>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["boolean", "int", "real", "const", "string", "struct"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_param(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Params>", [","], token_queue.peek())
            )
        # Predicting for production <Params>
        local_first_set = ["string", "boolean", "int", "const", "struct", "real"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_params(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production [<Param>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["boolean", "int", "real", "const", "string", "struct"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_param(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_while_procedure(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <While Procedure>\n
    Accepted productions below\n
    ['while', '(', <Conditional Expression>, ')', '{', <Body Procedure>, '}']\n
    """

    node = SynthaticNode(production="<While Procedure>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['while', '(', <Conditional Expression>, ')', '{', <Body Procedure>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "while":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While Procedure>", ["("], token_queue.peek())
            )
        # Predicting for production <Conditional Expression>
        local_first_set = ["!", "true", "false", "(", "local", "global", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_conditional_expression(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<While Procedure>", local_first_set, token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While Procedure>", [")"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While Procedure>", ["{"], token_queue.peek())
            )
        # Predicting for production <Body Procedure>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While Procedure>", ["}"], token_queue.peek())
            )

    return node


def sp_then(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Then>\n
    Accepted productions below\n
    [')', 'then', '{', <Body>, '}', <Else>]\n
    """

    node = SynthaticNode(production="<Then>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [')', 'then', '{', <Body>, '}', <Else>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "then":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Then>", ["then"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Then>", ["{"], token_queue.peek()))
        # Predicting for production <Body>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
            "return",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Then>", ["}"], token_queue.peek()))
        # Predicting for production <Else>
        local_first_set = ["else"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_else(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_if(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    """
    This function parse tokens for production <If>\n
    Accepted productions below\n
    ['if', '(', <Conditional Expression>, <Then>]\n
    """

    node = SynthaticNode(production="<If>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['if', '(', <Conditional Expression>, <Then>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "if":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<If>", ["("], token_queue.peek()))
        # Predicting for production <Conditional Expression>
        local_first_set = ["!", "true", "false", "(", "local", "global", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_conditional_expression(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<If>", local_first_set, token_queue.peek())
            )
        # Predicting for production <Then>
        local_first_set = [")"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_then(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<If>", local_first_set, token_queue.peek())
            )

    return node


def sp_body(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Body>\n
    Accepted productions below\n
    [<Body Item>, <Body>]\n
    []\n
    """

    node = SynthaticNode(production="<Body>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Body Item>, <Body>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in [
        "read",
        "true",
        "while",
        "var",
        "print",
        "return",
        "(",
        "global",
        "if",
        "-",
        "local",
        "false",
    ]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_body_item(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Body>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
            "return",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

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
    [struct, Identifier]\n
    [Identifier]\n
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

    # Predicting for production [struct, Identifier]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "struct":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Type>", ["Identifier"], token_queue.peek())
            )

    # Predicting for production [Identifier]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())

    return node


def sp_var_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Var Decl>\n
    Accepted productions below\n
    ['var', '{', <VariablesList>, '}']\n
    []\n
    """

    node = SynthaticNode(production="<Var Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['var', '{', <VariablesList>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "var":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Var Decl>", ["{"], token_queue.peek())
            )
        # Predicting for production <VariablesList>
        local_first_set = ["boolean", "int", "struct", "real", "string"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_variables_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Var Decl>", ["}"], token_queue.peek())
            )

    # Predicting for production []
    else:
        return node

    return node


def sp_assignment__matrix__aux_1(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assignment_matrix_aux1>\n
    Accepted productions below\n
    [<Assignment_vector_aux1>]\n
    """

    node = SynthaticNode(production="<Assignment_matrix_aux1>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Assignment_vector_aux1>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["="]:
        temp = sp_assignment__vector__aux_1(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_function_call(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Function Call>\n
    Accepted productions below\n
    [Identifier, '(', <Formal Parameter List>, ')']\n
    """

    node = SynthaticNode(production="<Function Call>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [Identifier, '(', <Formal Parameter List>, ')']
    if (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Function Call>", ["("], token_queue.peek())
            )
        # Predicting for production <Formal Parameter List>
        local_first_set = ["true", "(", "global", "false", "local", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_formal_parameter_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Function Call>", [")"], token_queue.peek())
            )

    return node


def sp_value__assigned__vector(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Value_assigned_vector>\n
    Accepted productions below\n
    [<Value>, ',', <Value_assigned_vector>]\n
    [<Value>]\n
    """

    node = SynthaticNode(production="<Value_assigned_vector>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Value>, ',', <Value_assigned_vector>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["false", "true"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_value(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Value_assigned_vector>", [","], token_queue.peek()
                )
            )
        # Predicting for production <Value_assigned_vector>
        local_first_set = ["true", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_value__assigned__vector(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Value_assigned_vector>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production [<Value>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["false", "true"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_value(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_index(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Index>\n
    Accepted productions below\n
    [DecLiteral]\n
    [OctLiteral]\n
    [Identifier]\n
    """

    node = SynthaticNode(production="<Index>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [DecLiteral]
    if token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER:
        node.add(token_queue.remove())

    # Predicting for production [OctLiteral]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER
    ):
        node.add(token_queue.remove())

    # Predicting for production [Identifier]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())

    return node


def sp_assignment__vector__aux_2(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assignment_vector_aux2>\n
    Accepted productions below\n
    ['=', '{', <Value_assigned_vector>, '}']\n
    """

    node = SynthaticNode(production="<Assignment_vector_aux2>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['=', '{', <Value_assigned_vector>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_vector_aux2>", ["{"], token_queue.peek()
                )
            )
        # Predicting for production <Value_assigned_vector>
        local_first_set = ["true", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_value__assigned__vector(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_vector_aux2>", local_first_set, token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_vector_aux2>", ["}"], token_queue.peek()
                )
            )

    return node


def sp_program(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Program>\n
    Accepted productions below\n
    [<Global Decl>, <Decls>, <Start>]\n
    """

    node = SynthaticNode(production="<Program>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Global Decl>, <Decls>, <Start>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["var", "const"]:
        temp = sp_global_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Decls>
    local_first_set = ["struct", "function", "procedure", "typedef"]
    temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
    token_verification = temp_token_type == TokenTypes.IDENTIFIER
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in local_first_set
            or token_verification
    ):
        temp = sp_decls(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Start>
    local_first_set = ["start"]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_start(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Program>", local_first_set, token_queue.peek())
            )

    return node


def sp_read(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Read>\n
    Accepted productions below\n
    ['read', '(', <Formal Parameter List Read>, ')', ';']\n
    """

    node = SynthaticNode(production="<Read>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['read', '(', <Formal Parameter List Read>, ')', ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "read":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Read>", ["("], token_queue.peek()))
        # Predicting for production <Formal Parameter List Read>
        local_first_set = []
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_formal_parameter_list_read(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Read>", local_first_set, token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Read>", [")"], token_queue.peek()))
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Read>", [";"], token_queue.peek()))

    return node


def sp_relational(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Relational>\n
    Accepted productions below\n
    ['>', <Exp>]\n
    ['<', <Exp>]\n
    ['<=', <Exp>]\n
    ['>=', <Exp>]\n
    ['==', <Exp>]\n
    ['!=', <Exp>]\n
    """

    node = SynthaticNode(production="<Relational>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['>', <Exp>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ">":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Relational>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production ['<', <Exp>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "<":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Relational>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production ['<=', <Exp>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "<=":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Relational>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production ['>=', <Exp>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == ">=":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Relational>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production ['==', <Exp>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "==":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Relational>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production ['!=', <Exp>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "!=":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Relational>", local_first_set, token_queue.peek()
                )
            )

    return node


def sp_else(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Else>\n
    Accepted productions below\n
    ['else', '{', <Body>, '}']\n
    []\n
    """

    node = SynthaticNode(production="<Else>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['else', '{', <Body>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "else":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Else>", ["{"], token_queue.peek()))
        # Predicting for production <Body>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
            "return",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(SynthaticParseErrors("<Else>", ["}"], token_queue.peek()))

    # Predicting for production []
    else:
        return node

    return node


def sp_assignment__vector(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assignment_vector>\n
    Accepted productions below\n
    [<Assignment_vector_aux1>]\n
    [<Assignment_vector_aux2>]\n
    []\n
    """

    node = SynthaticNode(production="<Assignment_vector>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Assignment_vector_aux1>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["="]:
        temp = sp_assignment__vector__aux_1(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Assignment_vector_aux2>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["="]:
        temp = sp_assignment__vector__aux_2(token_queue, error_list)
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
    ['const', '{', <ConstList>, '}']\n
    []\n
    """

    node = SynthaticNode(production="<Const Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['const', '{', <ConstList>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "const":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Const Decl>", ["{"], token_queue.peek())
            )
        # Predicting for production <ConstList>
        local_first_set = ["boolean", "int", "struct", "real", "string"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_const_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Const Decl>", ["}"], token_queue.peek())
            )

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
    ['procedure', Identifier, '(', <Params>, ')', '{', <Body Procedure>, '}']\n
    [Identifier, '(', <Formal Parameter List>, ')', '{', <Body Procedure>, '}']\n
    """

    node = SynthaticNode(production="<Proc Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['procedure', Identifier, '(', <Params>, ')', '{', <Body Procedure>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "procedure":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", ["Identifier"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", ["("], token_queue.peek())
            )
        # Predicting for production <Params>
        local_first_set = ["string", "boolean", "int", "const", "struct", "real"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
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
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", [")"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", ["{"], token_queue.peek())
            )
        # Predicting for production <Body Procedure>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", ["}"], token_queue.peek())
            )

    # Predicting for production [Identifier, '(', <Formal Parameter List>, ')', '{', <Body Procedure>, '}']
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", ["("], token_queue.peek())
            )
        # Predicting for production <Formal Parameter List>
        local_first_set = ["true", "(", "global", "false", "local", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_formal_parameter_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", [")"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", ["{"], token_queue.peek())
            )
        # Predicting for production <Body Procedure>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Proc Decl>", ["}"], token_queue.peek())
            )

    return node


def sp_value(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Value>\n
    Accepted productions below\n
    [<Number>]\n
    [<Boolean Literal>]\n
    [StringLiteral]\n
    """

    node = SynthaticNode(production="<Value>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Number>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in []
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_number(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Boolean Literal>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["true", "false"]:
        temp = sp_boolean_literal(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [StringLiteral]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.STRING
    ):
        node.add(token_queue.remove())

    return node


def sp_assign(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assign>\n
    Accepted productions below\n
    [<PrefixGlobalLocal>, Identifier, '=', <Exp>, ';']\n
    [Identifier, '=', <Exp>, ';']\n
    [Identifier, <Vector>, <Assignment_vector>, ';']\n
    [Identifier, <Matrix>, <Assignment_matrix>, ';']\n
    [<Exp>, ';']\n
    """

    node = SynthaticNode(production="<Assign>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<PrefixGlobalLocal>, Identifier, '=', <Exp>, ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["local", "global"]:
        temp = sp_prefix_global_local(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", ["Identifier"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", ["="], token_queue.peek())
            )
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", local_first_set, token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", [";"], token_queue.peek())
            )

    # Predicting for production [Identifier, '=', <Exp>, ';']
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", ["="], token_queue.peek())
            )
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", local_first_set, token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", [";"], token_queue.peek())
            )

    # Predicting for production [Identifier, <Vector>, <Assignment_vector>, ';']
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Vector>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_vector(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", local_first_set, token_queue.peek())
            )
        # Predicting for production <Assignment_vector>
        local_first_set = ["="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assignment__vector(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", [";"], token_queue.peek())
            )

    # Predicting for production [Identifier, <Matrix>, <Assignment_matrix>, ';']
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Matrix>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_matrix(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", local_first_set, token_queue.peek())
            )
        # Predicting for production <Assignment_matrix>
        local_first_set = ["="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assignment__matrix(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", [";"], token_queue.peek())
            )

    # Predicting for production [<Exp>, ';']
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "local", "global", "-", "false"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_exp(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Assign>", [";"], token_queue.peek())
            )

    return node


def sp_const(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Const>\n
    Accepted productions below\n
    [Identifier, '=', <Value>, <Delimiter Const>]\n
    """

    node = SynthaticNode(production="<Const>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [Identifier, '=', <Value>, <Delimiter Const>]
    if (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Const>", ["="], token_queue.peek())
            )
        # Predicting for production <Value>
        local_first_set = ["false", "true"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
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
            error_list.append(
                SynthaticParseErrors("<Const>", local_first_set, token_queue.peek())
            )
        # Predicting for production <Delimiter Const>
        local_first_set = [";", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_delimiter_const(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Const>", local_first_set, token_queue.peek())
            )

    return node


def sp_start(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Start>\n
    Accepted productions below\n
    ['start', '(', ')', '{', <Body Procedure>, '}', <Decls>]\n
    """

    node = SynthaticNode(production="<Start>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['start', '(', ')', '{', <Body Procedure>, '}', <Decls>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "start":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Start>", ["("], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Start>", [")"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Start>", ["{"], token_queue.peek())
            )
        # Predicting for production <Body Procedure>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Start>", ["}"], token_queue.peek())
            )
        # Predicting for production <Decls>
        local_first_set = ["struct", "function", "procedure", "typedef"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_conditional_expression(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Conditional Expression>\n
    Accepted productions below\n
    [<Boolean Literal>]\n
    [<Relational Expression>]\n
    [<Logical Expression>]\n
    """

    node = SynthaticNode(production="<Conditional Expression>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Boolean Literal>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["true", "false"]:
        temp = sp_boolean_literal(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Relational Expression>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "global", "false", "local", "-"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_relational_expression(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Logical Expression>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["!", "true", "false", "(", "local", "global", "-"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_logical_expression(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_variable(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Variable>\n
    Accepted productions below\n
    [Identifier, <Aux>]\n
    """

    node = SynthaticNode(production="<Variable>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [Identifier, <Aux>]
    if (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())
        # Predicting for production <Aux>
        local_first_set = ["=", "[", ";", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_aux(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Variable>", local_first_set, token_queue.peek())
            )

    return node


def sp_if_procedure(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <If Procedure>\n
    Accepted productions below\n
    ['if', '(', <Conditional Expression>, <Then Procedure>]\n
    """

    node = SynthaticNode(production="<If Procedure>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['if', '(', <Conditional Expression>, <Then Procedure>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "if":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<If Procedure>", ["("], token_queue.peek())
            )
        # Predicting for production <Conditional Expression>
        local_first_set = ["!", "true", "false", "(", "local", "global", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_conditional_expression(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<If Procedure>", local_first_set, token_queue.peek()
                )
            )
        # Predicting for production <Then Procedure>
        local_first_set = [")"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_then_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<If Procedure>", local_first_set, token_queue.peek()
                )
            )

    return node


def sp_boolean_literal(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Boolean Literal>\n
    Accepted productions below\n
    ['true']\n
    ['false']\n
    """

    node = SynthaticNode(production="<Boolean Literal>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['true']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "true":
        node.add(token_queue.remove())

    # Predicting for production ['false']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "false":
        node.add(token_queue.remove())

    return node


def sp_body_item(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Body Item>\n
    Accepted productions below\n
    [<Var Decl>]\n
    [<While>]\n
    [<If>]\n
    [<Read>]\n
    [<Print>]\n
    [<Assign>]\n
    [<Return Statement>]\n
    """

    node = SynthaticNode(production="<Body Item>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Var Decl>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["var"]:
        temp = sp_var_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<While>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["while"]:
        temp = sp_while(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<If>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["if"]:
        temp = sp_if(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Read>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["read"]:
        temp = sp_read(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Print>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["print"]:
        temp = sp_print(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Assign>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "local", "false", "global", "-"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_assign(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Return Statement>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["return"]:
        temp = sp_return_statement(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_exp(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    """
    This function parse tokens for production <Exp>\n
    Accepted productions below\n
    [<PrefixGlobalLocal>, <Term>, <Add Exp>]\n
    [<Term>, <Add Exp>]\n
    """

    node = SynthaticNode(production="<Exp>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<PrefixGlobalLocal>, <Term>, <Add Exp>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["local", "global"]:
        temp = sp_prefix_global_local(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Term>
        local_first_set = ["true", "(", "false", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_term(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Exp>", local_first_set, token_queue.peek())
            )
        # Predicting for production <Add Exp>
        local_first_set = ["-", "+"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_add_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production [<Term>, <Add Exp>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["true", "(", "false", "-"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_term(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Add Exp>
        local_first_set = ["-", "+"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_add_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_then_procedure(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Then Procedure>\n
    Accepted productions below\n
    [')', 'then', '{', <Body Procedure>, '}', <Else Procedure>]\n
    """

    node = SynthaticNode(production="<Then Procedure>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [')', 'then', '{', <Body Procedure>, '}', <Else Procedure>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "then":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Then Procedure>", ["then"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Then Procedure>", ["{"], token_queue.peek())
            )
        # Predicting for production <Body Procedure>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Then Procedure>", ["}"], token_queue.peek())
            )
        # Predicting for production <Else Procedure>
        local_first_set = ["else"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_else_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_body_item_procedure(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Body Item Procedure>\n
    Accepted productions below\n
    [<Var Decl>]\n
    [<While Procedure>]\n
    [<If Procedure>]\n
    [<Read>]\n
    [<Print>]\n
    [<Assign>]\n
    """

    node = SynthaticNode(production="<Body Item Procedure>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Var Decl>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["var"]:
        temp = sp_var_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<While Procedure>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["while"]:
        temp = sp_while_procedure(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<If Procedure>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["if"]:
        temp = sp_if_procedure(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Read>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["read"]:
        temp = sp_read(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Print>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["print"]:
        temp = sp_print(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Assign>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "local", "false", "global", "-"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_assign(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_typedef_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Typedef Decl>\n
    Accepted productions below\n
    [typedef, <Base>, Identifier, ';']\n
    """

    node = SynthaticNode(production="<Typedef Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [typedef, <Base>, Identifier, ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "typedef":
        node.add(token_queue.remove())
        # Predicting for production <Base>
        local_first_set = ["boolean", "int", "real", "string", "struct"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_base(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Typedef Decl>", local_first_set, token_queue.peek()
                )
            )
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Typedef Decl>", ["Identifier"], token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Typedef Decl>", [";"], token_queue.peek())
            )

    return node


def sp_logical_denied(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Logical Denied>\n
    Accepted productions below\n
    ['!', Identifier]\n
    ['!', <Boolean Literal>]\n
    ['!', <Logical Expression>]\n
    ['!', <Relational Expression>]\n
    """

    node = SynthaticNode(production="<Logical Denied>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['!', Identifier]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "!":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Logical Denied>", ["Identifier"], token_queue.peek()
                )
            )

    # Predicting for production ['!', <Boolean Literal>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "!":
        node.add(token_queue.remove())
        # Predicting for production <Boolean Literal>
        local_first_set = ["true", "false"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_boolean_literal(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Logical Denied>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production ['!', <Logical Expression>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "!":
        node.add(token_queue.remove())
        # Predicting for production <Logical Expression>
        local_first_set = ["!", "true", "false", "(", "local", "global", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_logical_expression(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Logical Denied>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production ['!', <Relational Expression>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "!":
        node.add(token_queue.remove())
        # Predicting for production <Relational Expression>
        local_first_set = ["true", "(", "global", "false", "local", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_relational_expression(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Logical Denied>", local_first_set, token_queue.peek()
                )
            )

    return node


def sp_print(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Print>\n
    Accepted productions below\n
    [print, '(', <Formal Parameter List>, ')', ';']\n
    """

    node = SynthaticNode(production="<Print>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [print, '(', <Formal Parameter List>, ')', ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "print":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Print>", ["("], token_queue.peek())
            )
        # Predicting for production <Formal Parameter List>
        local_first_set = ["true", "(", "global", "false", "local", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_formal_parameter_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Print>", [")"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Print>", [";"], token_queue.peek())
            )

    return node


def sp_variables_list(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <VariablesList>\n
    Accepted productions below\n
    [<Type>, <Variable>, <VariablesList>]\n
    []\n
    """

    node = SynthaticNode(production="<VariablesList>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Type>, <Variable>, <VariablesList>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["boolean", "int", "struct", "string", "real"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Variable>
        local_first_set = []
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_variable(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<VariablesList>", local_first_set, token_queue.peek()
                )
            )
        # Predicting for production <VariablesList>
        local_first_set = ["boolean", "int", "struct", "real", "string"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_variables_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_global_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Global Decl>\n
    Accepted productions below\n
    [<Const Decl>, <Var Decl>]\n
    [<Var Decl>, <Const Decl>]\n
    []\n
    """

    node = SynthaticNode(production="<Global Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Const Decl>, <Var Decl>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["const"]:
        temp = sp_const_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Var Decl>
    local_first_set = ["var"]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_var_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Var Decl>, <Const Decl>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["var"]:
        temp = sp_var_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
    # Predicting for production <Const Decl>
    local_first_set = ["const"]
    if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
        temp = sp_const_decl(token_queue, error_list)
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
    [const, <Type>, Identifier]\n
    [<Type>, Identifier]\n
    """

    node = SynthaticNode(production="<Param>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [const, <Type>, Identifier]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "const":
        node.add(token_queue.remove())
        # Predicting for production <Type>
        local_first_set = ["boolean", "int", "struct", "string", "real"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_type(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Param>", local_first_set, token_queue.peek())
            )
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Param>", ["Identifier"], token_queue.peek())
            )

    # Predicting for production [<Type>, Identifier]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["boolean", "int", "struct", "string", "real"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Param>", ["Identifier"], token_queue.peek())
            )

    return node


def sp_else_procedure(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Else Procedure>\n
    Accepted productions below\n
    ['else', '{', <Body Procedure>, '}']\n
    []\n
    """

    node = SynthaticNode(production="<Else Procedure>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['else', '{', <Body Procedure>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "else":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Else Procedure>", ["{"], token_queue.peek())
            )
        # Predicting for production <Body Procedure>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Else Procedure>", ["}"], token_queue.peek())
            )

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
    ['extends', Identifier]\n
    []\n
    """

    node = SynthaticNode(production="<Extends>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['extends', Identifier]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "extends":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Extends>", ["Identifier"], token_queue.peek())
            )

    # Predicting for production []
    else:
        return node

    return node


def sp_vector(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Vector>\n
    Accepted productions below\n
    ['[', <Index>, ']']\n
    """

    node = SynthaticNode(production="<Vector>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['[', <Index>, ']']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "[":
        node.add(token_queue.remove())
        # Predicting for production <Index>
        local_first_set = []
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_index(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Vector>", local_first_set, token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "]":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Vector>", ["]"], token_queue.peek())
            )

    return node


def sp_delimiter_var(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Delimiter Var>\n
    Accepted productions below\n
    [',', <Variable>]\n
    [';']\n
    """

    node = SynthaticNode(production="<Delimiter Var>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Variable>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Variable>
        local_first_set = []
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_variable(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Delimiter Var>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production [';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == ";":
        node.add(token_queue.remove())

    return node


def sp_expression_value(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Expression Value>\n
    Accepted productions below\n
    ['-', <Expression Value>]\n
    [Identifier]\n
    ['(', <Exp>, ')']\n
    [<Number>]\n
    [<Boolean Literal>]\n
    [StringLiteral]\n
    [<Function Call>]\n
    """

    node = SynthaticNode(production="<Expression Value>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['-', <Expression Value>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "-":
        node.add(token_queue.remove())
        # Predicting for production <Expression Value>
        local_first_set = ["true", "(", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_expression_value(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Expression Value>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production [Identifier]
    elif (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())

    # Predicting for production ['(', <Exp>, ')']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "(":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Expression Value>", local_first_set, token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Expression Value>", [")"], token_queue.peek())
            )

    # Predicting for production [<Number>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in []
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_number(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Boolean Literal>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["true", "false"]:
        temp = sp_boolean_literal(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [StringLiteral]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.STRING
    ):
        node.add(token_queue.remove())

    # Predicting for production [<Function Call>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in []
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_function_call(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_aux(token_queue: Queue, error_list: list[SynthaticParseErrors]) -> SynthaticNode:
    """
    This function parse tokens for production <Aux>\n
    Accepted productions below\n
    ['=', <Value>, <Delimiter Var>]\n
    [<Delimiter Var>]\n
    [<Vector>, <Assignment_vector>, <Delimiter Var>]\n
    [<Matrix>, <Assignment_matrix>, <Delimiter Var>]\n
    """

    node = SynthaticNode(production="<Aux>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['=', <Value>, <Delimiter Var>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
        node.add(token_queue.remove())
        # Predicting for production <Value>
        local_first_set = ["false", "true"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
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
            error_list.append(
                SynthaticParseErrors("<Aux>", local_first_set, token_queue.peek())
            )
        # Predicting for production <Delimiter Var>
        local_first_set = [";", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_delimiter_var(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Aux>", local_first_set, token_queue.peek())
            )

    # Predicting for production [<Delimiter Var>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in [";", ","]:
        temp = sp_delimiter_var(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Vector>, <Assignment_vector>, <Delimiter Var>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["["]:
        temp = sp_vector(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Assignment_vector>
        local_first_set = ["="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assignment__vector(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        # Predicting for production <Delimiter Var>
        local_first_set = [";", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_delimiter_var(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Aux>", local_first_set, token_queue.peek())
            )

    # Predicting for production [<Matrix>, <Assignment_matrix>, <Delimiter Var>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["["]:
        temp = sp_matrix(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Assignment_matrix>
        local_first_set = ["="]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_assignment__matrix(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        # Predicting for production <Delimiter Var>
        local_first_set = [";", ","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_delimiter_var(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Aux>", local_first_set, token_queue.peek())
            )

    return node


def sp_dimensao__matrix_2(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Dimensao_matrix2>\n
    Accepted productions below\n
    [',', '{', <Value_assigned_matrix>, '}', '}']\n
    """

    node = SynthaticNode(production="<Dimensao_matrix2>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', '{', <Value_assigned_matrix>, '}', '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Dimensao_matrix2>", ["{"], token_queue.peek())
            )
        # Predicting for production <Value_assigned_matrix>
        local_first_set = ["true", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_value__assigned__matrix(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Dimensao_matrix2>", local_first_set, token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Dimensao_matrix2>", ["}"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Dimensao_matrix2>", ["}"], token_queue.peek())
            )

    return node


def sp_term(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Term>\n
    Accepted productions below\n
    [<Expression Value>, <Mult Exp>]\n
    """

    node = SynthaticNode(production="<Term>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Expression Value>, <Mult Exp>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["true", "(", "-", "false"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_expression_value(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Mult Exp>
        local_first_set = ["*", "/"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_mult_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    return node


def sp_add_exp(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Add Exp>\n
    Accepted productions below\n
    ['+', <Exp>]\n
    ['-', <Exp>]\n
    []\n
    """

    node = SynthaticNode(production="<Add Exp>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['+', <Exp>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "+":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Add Exp>", local_first_set, token_queue.peek())
            )

    # Predicting for production ['-', <Exp>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "-":
        node.add(token_queue.remove())
        # Predicting for production <Exp>
        local_first_set = ["true", "(", "local", "global", "-", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_exp(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Add Exp>", local_first_set, token_queue.peek())
            )

    # Predicting for production []
    else:
        return node

    return node


def sp_body_procedure(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Body Procedure>\n
    Accepted productions below\n
    [<Body Item Procedure>, <Body Procedure>]\n
    []\n
    """

    node = SynthaticNode(production="<Body Procedure>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Body Item Procedure>, <Body Procedure>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in [
        "read",
        "true",
        "while",
        "var",
        "print",
        "(",
        "global",
        "if",
        "-",
        "local",
        "false",
    ]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_body_item_procedure(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Body Procedure>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body_procedure(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_assignment__matrix__aux_2(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assignment_matrix_aux2>\n
    Accepted productions below\n
    ['=', '{', '{', <Value_assigned_matrix>, '}', <Dimensao_matrix2>]\n
    """

    node = SynthaticNode(production="<Assignment_matrix_aux2>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['=', '{', '{', <Value_assigned_matrix>, '}', <Dimensao_matrix2>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_matrix_aux2>", ["{"], token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_matrix_aux2>", ["{"], token_queue.peek()
                )
            )
        # Predicting for production <Value_assigned_matrix>
        local_first_set = ["true", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_value__assigned__matrix(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_matrix_aux2>", local_first_set, token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_matrix_aux2>", ["}"], token_queue.peek()
                )
            )
        # Predicting for production <Dimensao_matrix2>
        local_first_set = [","]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_dimensao__matrix_2(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_matrix_aux2>", local_first_set, token_queue.peek()
                )
            )

    return node


def sp_prefix_global_local(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <PrefixGlobalLocal>\n
    Accepted productions below\n
    ['global', '.']\n
    ['local', '.']\n
    """

    node = SynthaticNode(production="<PrefixGlobalLocal>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['global', '.']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "global":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == ".":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<PrefixGlobalLocal>", ["."], token_queue.peek())
            )

    # Predicting for production ['local', '.']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "local":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == ".":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<PrefixGlobalLocal>", ["."], token_queue.peek())
            )

    return node


def sp_expression_value_logical(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Expression Value Logical>\n
    Accepted productions below\n
    [Identifier]\n
    [<Boolean Literal>]\n
    [StringLiteral]\n
    [<Function Call>]\n
    [<Relational Expression>]\n
    """

    node = SynthaticNode(production="<Expression Value Logical>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [Identifier]
    if (
            token_queue.peek()
            and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
    ):
        node.add(token_queue.remove())

    # Predicting for production [<Boolean Literal>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["true", "false"]:
        temp = sp_boolean_literal(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [StringLiteral]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.STRING
    ):
        node.add(token_queue.remove())

    # Predicting for production [<Function Call>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in []
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_function_call(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Relational Expression>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "global", "false", "local", "-"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_relational_expression(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_matrix(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Matrix>\n
    Accepted productions below\n
    ['[', <Index>, ']', <Vector>]\n
    """

    node = SynthaticNode(production="<Matrix>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['[', <Index>, ']', <Vector>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "[":
        node.add(token_queue.remove())
        # Predicting for production <Index>
        local_first_set = []
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_index(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Matrix>", local_first_set, token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "]":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Matrix>", ["]"], token_queue.peek())
            )
        # Predicting for production <Vector>
        local_first_set = ["["]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_vector(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Matrix>", local_first_set, token_queue.peek())
            )

    return node


def sp_mult_exp(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Mult Exp>\n
    Accepted productions below\n
    ['*', <Term>]\n
    ['/', <Term>]\n
    []\n
    """

    node = SynthaticNode(production="<Mult Exp>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['*', <Term>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "*":
        node.add(token_queue.remove())
        # Predicting for production <Term>
        local_first_set = ["true", "(", "false", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_term(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Mult Exp>", local_first_set, token_queue.peek())
            )

    # Predicting for production ['/', <Term>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "/":
        node.add(token_queue.remove())
        # Predicting for production <Term>
        local_first_set = ["true", "(", "false", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_term(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Mult Exp>", local_first_set, token_queue.peek())
            )

    # Predicting for production []
    else:
        return node

    return node


def sp_while(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <While>\n
    Accepted productions below\n
    ['while', '(', <Conditional Expression>, ')', '{', <Body>, '}']\n
    """

    node = SynthaticNode(production="<While>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['while', '(', <Conditional Expression>, ')', '{', <Body>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "while":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While>", ["("], token_queue.peek())
            )
        # Predicting for production <Conditional Expression>
        local_first_set = ["!", "true", "false", "(", "local", "global", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_conditional_expression(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<While>", local_first_set, token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == ")":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While>", [")"], token_queue.peek())
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While>", ["{"], token_queue.peek())
            )
        # Predicting for production <Body>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
            "return",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<While>", ["}"], token_queue.peek())
            )

    return node


def sp_function_declaration(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Function Declaration>\n
    Accepted productions below\n
    ['function', <Type>, Identifier, '(', <Params>, ')', '{', <Body>, '}']\n
    """

    node = SynthaticNode(production="<Function Declaration>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['function', <Type>, Identifier, '(', <Params>, ')', '{', <Body>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "function":
        node.add(token_queue.remove())
        # Predicting for production <Type>
        local_first_set = ["boolean", "int", "struct", "string", "real"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_type(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Function Declaration>", local_first_set, token_queue.peek()
                )
            )
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Function Declaration>", ["Identifier"], token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "(":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Function Declaration>", ["("], token_queue.peek()
                )
            )
        # Predicting for production <Params>
        local_first_set = ["string", "boolean", "int", "const", "struct", "real"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
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
            error_list.append(
                SynthaticParseErrors(
                    "<Function Declaration>", [")"], token_queue.peek()
                )
            )
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Function Declaration>", ["{"], token_queue.peek()
                )
            )
        # Predicting for production <Body>
        local_first_set = [
            "read",
            "true",
            "while",
            "var",
            "print",
            "false",
            "if",
            "(",
            "global",
            "local",
            "-",
            "return",
        ]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_body(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Function Declaration>", ["}"], token_queue.peek()
                )
            )

    return node


def sp_logical(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Logical>\n
    Accepted productions below\n
    [<Conditional Operator>, <Expression Value Logical>]\n
    [<Conditional Operator>, <Logical Denied>]\n
    """

    node = SynthaticNode(production="<Logical>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Conditional Operator>, <Expression Value Logical>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["||", "&&"]:
        temp = sp_conditional_operator(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Expression Value Logical>
        local_first_set = ["true", "false", "(", "global", "local", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_expression_value_logical(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Logical>", local_first_set, token_queue.peek())
            )

    # Predicting for production [<Conditional Operator>, <Logical Denied>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["||", "&&"]:
        temp = sp_conditional_operator(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Logical Denied>
        local_first_set = ["!"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_logical_denied(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors("<Logical>", local_first_set, token_queue.peek())
            )

    return node


def sp_formal_parameter_list(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Formal Parameter List>\n
    Accepted productions below\n
    [<Exp>]\n
    [<Exp>, ',', <Formal Parameter List>]\n
    []\n
    """

    node = SynthaticNode(production="<Formal Parameter List>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Exp>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "local", "global", "-", "false"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_exp(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Exp>, ',', <Formal Parameter List>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "(", "local", "global", "-", "false"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.STRING
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
    ):
        temp = sp_exp(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Formal Parameter List>", [","], token_queue.peek()
                )
            )
        # Predicting for production <Formal Parameter List>
        local_first_set = ["true", "(", "global", "false", "local", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_formal_parameter_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_logical_expression(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Logical Expression>\n
    Accepted productions below\n
    [<Expression Value Logical>, <Logical>]\n
    [<Logical Denied>]\n
    """

    node = SynthaticNode(production="<Logical Expression>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Expression Value Logical>, <Logical>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["true", "false", "(", "global", "local", "-"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.IDENTIFIER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_expression_value_logical(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Logical>
        local_first_set = ["||", "&&"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_logical(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Logical Expression>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production [<Logical Denied>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["!"]:
        temp = sp_logical_denied(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_return_statement(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Return Statement>\n
    Accepted productions below\n
    ['return', ';']\n
    ['return', <Assign>]\n
    """

    node = SynthaticNode(production="<Return Statement>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['return', ';']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "return":
        node.add(token_queue.remove())
        if token_queue.peek() and token_queue.peek().get_lexeme() == ";":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Return Statement>", [";"], token_queue.peek())
            )

    # Predicting for production ['return', <Assign>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() == "return":
        node.add(token_queue.remove())
        # Predicting for production <Assign>
        local_first_set = ["true", "(", "local", "false", "global", "-"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.IDENTIFIER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_assign(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Return Statement>", local_first_set, token_queue.peek()
                )
            )

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
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["struct", "function", "procedure", "typedef"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Decls>
        local_first_set = ["struct", "function", "procedure", "typedef"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_decls(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_const_list(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <ConstList>\n
    Accepted productions below\n
    [<Type>, <Const>, <ConstList>]\n
    []\n
    """

    node = SynthaticNode(production="<ConstList>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Type>, <Const>, <ConstList>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme()
            in ["boolean", "int", "struct", "string", "real"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_type(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        # Predicting for production <Const>
        local_first_set = []
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
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
            error_list.append(
                SynthaticParseErrors("<ConstList>", local_first_set, token_queue.peek())
            )
        # Predicting for production <ConstList>
        local_first_set = ["boolean", "int", "struct", "real", "string"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_const_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_number(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Number>\n
    Accepted productions below\n
    [DecLiteral]\n
    [OctLiteral]\n
    [HexLiteral]\n
    [FloatLiteral]\n
    """

    node = SynthaticNode(production="<Number>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [DecLiteral]
    if token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER:
        node.add(token_queue.remove())

    # Predicting for production [OctLiteral]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER
    ):
        node.add(token_queue.remove())

    # Predicting for production [HexLiteral]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER
    ):
        node.add(token_queue.remove())

    # Predicting for production [FloatLiteral]
    elif (
            token_queue.peek() and token_queue.peek().get_token_type() == TokenTypes.NUMBER
    ):
        node.add(token_queue.remove())

    return node


def sp_struct_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Struct Decl>\n
    Accepted productions below\n
    [struct, Identifier, <Extends>, '{', <VariablesList>, '}']\n
    """

    node = SynthaticNode(production="<Struct Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [struct, Identifier, <Extends>, '{', <VariablesList>, '}']
    if token_queue.peek() and token_queue.peek().get_lexeme() == "struct":
        node.add(token_queue.remove())
        if (
                token_queue.peek()
                and token_queue.peek().get_token_type() == TokenTypes.IDENTIFIER
        ):
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Struct Decl>", ["Identifier"], token_queue.peek()
                )
            )
        # Predicting for production <Extends>
        local_first_set = ["extends"]
        if token_queue.peek() and token_queue.peek().get_lexeme() in local_first_set:
            temp = sp_extends(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "{":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Struct Decl>", ["{"], token_queue.peek())
            )
        # Predicting for production <VariablesList>
        local_first_set = ["boolean", "int", "struct", "real", "string"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = temp_token_type == TokenTypes.IDENTIFIER
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_variables_list(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == "}":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors("<Struct Decl>", ["}"], token_queue.peek())
            )

    return node


def sp_assignment__matrix(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assignment_matrix>\n
    Accepted productions below\n
    [<Assignment_matrix_aux1>]\n
    [<Assignment_matrix_aux2>]\n
    []\n
    """

    node = SynthaticNode(production="<Assignment_matrix>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Assignment_matrix_aux1>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["="]:
        temp = sp_assignment__matrix__aux_1(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Assignment_matrix_aux2>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["="]:
        temp = sp_assignment__matrix__aux_2(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production []
    else:
        return node

    return node


def sp_value__assigned__matrix(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Value_assigned_matrix>\n
    Accepted productions below\n
    [<Value>, ',', <Value_assigned_matrix>]\n
    [<Value>]\n
    """

    node = SynthaticNode(production="<Value_assigned_matrix>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Value>, ',', <Value_assigned_matrix>]
    if (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["false", "true"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_value(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)
        if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
            node.add(token_queue.remove())
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Value_assigned_matrix>", [","], token_queue.peek()
                )
            )
        # Predicting for production <Value_assigned_matrix>
        local_first_set = ["true", "false"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.STRING
        )
        if (
                token_queue.peek()
                and token_queue.peek().get_lexeme() in local_first_set
                or token_verification
        ):
            temp = sp_value__assigned__matrix(token_queue, error_list)
            if temp and temp.is_not_empty():
                node.add(temp)
        else:
            error_list.append(
                SynthaticParseErrors(
                    "<Value_assigned_matrix>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production [<Value>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["false", "true"]
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.NUMBER
            or temp_token_type == TokenTypes.STRING
    ):
        temp = sp_value(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_decl(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Decl>\n
    Accepted productions below\n
    [<Function Declaration>]\n
    [<Proc Decl>]\n
    [<Struct Decl>]\n
    [<Typedef Decl>]\n
    """

    node = SynthaticNode(production="<Decl>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [<Function Declaration>]
    if token_queue.peek() and token_queue.peek().get_lexeme() in ["function"]:
        temp = sp_function_declaration(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Proc Decl>]
    elif (
            token_queue.peek()
            and token_queue.peek().get_lexeme() in ["procedure"]
            or temp_token_type == TokenTypes.IDENTIFIER
    ):
        temp = sp_proc_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Struct Decl>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["struct"]:
        temp = sp_struct_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    # Predicting for production [<Typedef Decl>]
    elif token_queue.peek() and token_queue.peek().get_lexeme() in ["typedef"]:
        temp = sp_typedef_decl(token_queue, error_list)
        if temp and temp.is_not_empty():
            node.add(temp)

    return node


def sp_delimiter_const(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Delimiter Const>\n
    Accepted productions below\n
    [',', <Const>]\n
    [';']\n
    """

    node = SynthaticNode(production="<Delimiter Const>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production [',', <Const>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == ",":
        node.add(token_queue.remove())
        # Predicting for production <Const>
        local_first_set = []
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
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
            error_list.append(
                SynthaticParseErrors(
                    "<Delimiter Const>", local_first_set, token_queue.peek()
                )
            )

    # Predicting for production [';']
    elif token_queue.peek() and token_queue.peek().get_lexeme() == ";":
        node.add(token_queue.remove())

    return node


def sp_assignment__vector__aux_1(
        token_queue: Queue, error_list: list[SynthaticParseErrors]
) -> SynthaticNode:
    """
    This function parse tokens for production <Assignment_vector_aux1>\n
    Accepted productions below\n
    ['=', <Value>]\n
    """

    node = SynthaticNode(production="<Assignment_vector_aux1>")
    if not token_queue.peek():
        return node
    temp_token_type = token_queue.peek().get_token_type()
    # Predicting for production ['=', <Value>]
    if token_queue.peek() and token_queue.peek().get_lexeme() == "=":
        node.add(token_queue.remove())
        # Predicting for production <Value>
        local_first_set = ["false", "true"]
        temp_token_type = token_queue.peek() and token_queue.peek().get_token_type()
        token_verification = (
                temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
                or temp_token_type == TokenTypes.NUMBER
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
            error_list.append(
                SynthaticParseErrors(
                    "<Assignment_vector_aux1>", local_first_set, token_queue.peek()
                )
            )

    return node


productions_functions = {
    EProduction.START: sp_program
}
