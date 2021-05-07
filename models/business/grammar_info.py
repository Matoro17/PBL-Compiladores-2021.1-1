class FirstFollow:
    def __init__(self):
        self.CaseSensitive = "True"
        self.StartSymbol = "<Program>"
        self.__first = {
            "<Start>": ("start"),
            "<Proc Decl>": ("Identifier", "procedure"),
            "<Param>": ("int", "boolean", "string", "struct", "Identifier", "real", "const"),
            "<Assignment_matrix_aux1>": ("="),
            "<Value_assigned_vector>": (
                "StringLiteral", "DecLiteral", "FloatLiteral", "false", "true", "HexLiteral", "OctLiteral"),
            "<Body Item>": (
                "FloatLiteral", "var", "HexLiteral", "StringLiteral", "(", "if", "while", "true", "false", "global.",
                "Identifier", "OctLiteral", "-", "DecLiteral", "local.", "return", "print(", "read("),
            "<Expression Value Logical>": (
                "DecLiteral", "true", "HexLiteral", "global.", "Identifier", "false", "-", "StringLiteral", "local.",
                "FloatLiteral", "(", "OctLiteral"),
            "<PrefixGlobalLocal>": ("local.", "global."),
            "<Function Call>": ("Identifier"),
            "<Body Item Procedure>": (
                "FloatLiteral", "var", "HexLiteral", "StringLiteral", "(", "if", "while", "true", "global.",
                "Identifier",
                "OctLiteral", "-", "DecLiteral", "local.", "false", "print(", "read("),
            "<Body>": (
                "", "FloatLiteral", "var", "HexLiteral", "StringLiteral", "(", "if", "while", "true", "read(",
                "global.",
                "Identifier", "print(", "-", "false", "local.", "return", "OctLiteral", "DecLiteral"),
            "<Relational>": ("<=", "!=", "==", ">", ">=", "<"),
            "<Conditional Expression>": (
                "DecLiteral", "!", "true", "HexLiteral", "global.", "Identifier", "OctLiteral", "-", "StringLiteral",
                "local.", "FloatLiteral", "(", "false"),
            "<While>": ("while"),
            "<Number>": ("FloatLiteral", "OctLiteral", "HexLiteral", "DecLiteral"),
            "<Base>": ("Identifier", "boolean", "string", "struct", "real", "int"),
            "<Assignment_matrix_aux2>": ("="),
            "<Vector>": ("["),
            "<Index>": ("DecLiteral|"),
            "<Return Statement>": ("return"),
            "<Matrix>": ("["),
            "<Logical Denied>": ("!"),
            "<Conditional Operator>": ("&&", "||"),
            "<Formal Parameter List>": (
                "", "DecLiteral", "true", "HexLiteral", "global.", "Identifier", "OctLiteral", "-", "FloatLiteral",
                "local.", "false", "(", "StringLiteral"),
            "<Variable>": ("Identifier"),
            "<Then Procedure>": (")"),
            "<ConstList>": ("Identifier", "boolean", "string", "", "struct", "real", "int"),
            "<Function Declaration>": ("function"),
            "<Const>": ("Identifier"),
            "<Read>": ("read("),
            "<Dimensao_matrix2>": (","),
            "<Relational Expression>": (
                "DecLiteral", "true", "HexLiteral", "global.", "Identifier", "OctLiteral", "-", "FloatLiteral",
                "local.",
                "false", "(", "StringLiteral"),
            "<Delimiter Var>": (";", ","),
            "<Global Decl>": ("var", "", "const"),
            "<Assign>": (
                "DecLiteral", "true", "HexLiteral", "global.", "Identifier", "StringLiteral", "-", "FloatLiteral",
                "local.",
                "false", "(", "OctLiteral"),
            "<VariablesList>": ("Identifier", "boolean", "string", "", "struct", "real", "int"),
            "<Logical Expression>": (
                "DecLiteral", "!", "true", "HexLiteral", "global.", "Identifier", "StringLiteral", "-", "OctLiteral",
                "local.", "FloatLiteral", "(", "false"),
            "<Value>": ("OctLiteral", "StringLiteral", "FloatLiteral", "false", "true", "HexLiteral", "DecLiteral"),
            "<Exp>": (
                "DecLiteral", "true", "HexLiteral", "global.", "Identifier", "StringLiteral", "-", "OctLiteral",
                "local.",
                "false", "(", "FloatLiteral"),
            "<Else Procedure>": ("else", ""),
            "<Type>": ("int", "boolean", "string", "Identifier", "real", "struct"),
            "<Assignment_matrix>": ("=", ""),
            "<Delimiter Const>": (";", ","),
            "<If Procedure>": ("if"),
            "<Formal Parameter List Read>": ("Identifier"),
            "<If>": ("if"),
            "<Const Decl>": ("const"),
            "<Boolean Literal>": ("false", "true"),
            "<Assignment_vector>": ("=", ""),
            "<Decls>": ("Identifier", "struct", "", "typedef", "function", "procedure"),
            "<Program>": ("Identifier", "struct", "const", "var", "typedef", "function", "procedure"),
            "<Aux>": ("[", ";", "=", ","),
            "<Value_assigned_matrix>": (
                "StringLiteral", "DecLiteral", "FloatLiteral", "false", "true", "HexLiteral", "OctLiteral"),
            "<Params>": ("int", "struct", "string", "", "const", "Identifier", "real", "boolean"),
            "<While Procedure>": ("while"),
            "<Body Procedure>": (
                "", "FloatLiteral", "var", "HexLiteral", "OctLiteral", "(", "if", "while", "true", "global.",
                "Identifier",
                "read(", "-", "print(", "local.", "false", "StringLiteral", "DecLiteral"),
            "<Else>": ("else", ""),
            "<Mult Exp>": ("/", "", "*"),
            "<Logical>": ("&&", "||"),
            "<Extends>": ("", "extends"),
            "<Add Exp>": ("+", "-", ""),
            "<Assignment_vector_aux1>": ("="),
            "<Assignment_vector_aux2>": ("="),
            "<Typedef Decl>": ("typedef"),
            "<Decl>": ("Identifier", "struct", "typedef", "function", "procedure"),
            "<Print>": ("print("),
            "<Then>": (")"),
            "<Struct Decl>": ("struct"),
            "<Term>": (
                "DecLiteral", "true", "HexLiteral", "Identifier", "StringLiteral", "-", "FloatLiteral", "false", "(",
                "OctLiteral"),
            "<Var Decl>": ("var"),
            "<Expression Value>": (
                "DecLiteral", "true", "HexLiteral", "Identifier", "false", "-", "StringLiteral", "OctLiteral", "(",
                "FloatLiteral")
        }
        self.__follow = {
            "<Start>": ("$"),
            "<Proc Decl>": ("Identifier", "struct", "typedef", "function", "procedure"),
            "<Param>": ("Identifier", "procedure", "function", ","),
            "<Assignment_matrix_aux1>": (
                "DecLiteral", ";", "OctLiteral", "FloatLiteral", "false", "true", "=", "global.", "Identifier", "[",
                "-",
                ",", "local.", "StringLiteral", "(", "HexLiteral"),
            "<Value_assigned_vector>": ("="),
            "<Body Item>": (
                "FloatLiteral", "var", "HexLiteral", "false", "(", "if", "while", "true", "DecLiteral", "global.",
                "Identifier", "OctLiteral", "read(", "print(", "local.", "return", "-", "StringLiteral"),
            "<Expression Value Logical>": ("if", "||", "&&", "while"),
            "<PrefixGlobalLocal>": (
                "FloatLiteral", "true", "HexLiteral", "Identifier", "false", "-", "OctLiteral", "StringLiteral", "(",
                "DecLiteral"),
            "<Function Call>": ("/", "&&", "while", "*", "||", "if"),
            "<Body Item Procedure>": (
                "print(", "var", "HexLiteral", "OctLiteral", "(", "if", "while", "true", "global.", "Identifier",
                "DecLiteral", "-", "StringLiteral", "local.", "false", "FloatLiteral", "read("),
            "<Body>": ("while", "else", "function", ")"),
            "<Relational>": ("if", "||", "&&", "while"),
            "<Conditional Expression>": ("if", "while"),
            "<While>": ("print(", "var", "HexLiteral", "false", "(", "if", "while", "true", "StringLiteral", "global.",
                        "Identifier", "-", "read(", "DecLiteral", "local.", "return", "OctLiteral", "FloatLiteral"),
            "<Number>": ("/", "[", ",", "*", ";", "=", "Identifier"),
            "<Base>": ("typedef"),
            "<Assignment_matrix_aux2>": (
                "DecLiteral", ";", "OctLiteral", "FloatLiteral", "false", "true", "=", "global.", "Identifier", "[",
                "-",
                ",", "local.", "StringLiteral", "(", "HexLiteral"),
            "<Vector>": (
                "DecLiteral", "OctLiteral", "true", "=", "global.", "Identifier", "StringLiteral", "-", "FloatLiteral",
                "local.", "false", "(", "HexLiteral"),
            "<Index>": ("["),
            "<Value_assigned_matrix>": ("=", ","),
            "<Matrix>": (
                "FloatLiteral", "=", "true", "HexLiteral", "global.", "Identifier", "StringLiteral", "-", "OctLiteral",
                "local.", "false", "(", "DecLiteral"),
            "<Logical Denied>": ("if", "while"),
            "<Conditional Operator>": (
                "DecLiteral", "!", "true", "HexLiteral", "global.", "Identifier", "StringLiteral", "-", "OctLiteral",
                "local.", "FloatLiteral", "(", "false"),
            "<Else>": (),
            "<Variable>": ("Identifier", "struct", "string", "var", "int", "real", "boolean"),
            "<Then Procedure>": (
                "FloatLiteral", "var", "HexLiteral", "StringLiteral", "(", "if", "while", "true", "global.",
                "Identifier",
                "DecLiteral", "-", "OctLiteral", "local.", "false", "print(", "read("),
            "<ConstList>": ("const"),
            "<Function Declaration>": ("Identifier", "struct", "typedef", "function", "procedure"),
            "<Const>": ("Identifier", "struct", "string", "const", "int", "real", "boolean"),
            "<Read>": ("print(", "var", "HexLiteral", "false", "(", "if", "while", "true", "StringLiteral", "global.",
                       "Identifier", "-", "read(", "DecLiteral", "local.", "return", "OctLiteral", "FloatLiteral"),
            "<Dimensao_matrix2>": (),
            "<Relational Expression>": ("if", "||", "&&", "while"),
            "<Delimiter Var>": (),
            "<Global Decl>": ("Identifier", "struct", "typedef", "function", "procedure"),
            "<Assign>": ("print(", "var", "HexLiteral", "StringLiteral", "(", "if", "while", "true", "false", "global.",
                         "Identifier", "read(", "-", "FloatLiteral", "local.", "return", "OctLiteral", "DecLiteral"),
            "<VariablesList>": ("Identifier", "boolean", "string", "var", "int", "real", "struct"),
            "<Logical Expression>": ("if", "while"),
            "<Value>": (
                "HexLiteral", ";", "[", "DecLiteral", "StringLiteral", "true", "=", "global.", "Identifier",
                "OctLiteral",
                "-", ",", "local.", "false", "(", "FloatLiteral"),
            "<Exp>": (
                "FloatLiteral", ">", "HexLiteral", "<", "OctLiteral", "<=", "==", ">=", "(", "while", "if", ";", "&&",
                "DecLiteral", "||", "true", "print(", "global.", "Identifier", "procedure", "-", ",", "local.", "!=",
                "StringLiteral", "false"),
            "<Boolean Literal>": (
                "FloatLiteral", "HexLiteral", "[", "*", "||", "(", "if", ";", "false", "while", "DecLiteral", "true",
                "-",
                "global.", "Identifier", "OctLiteral", "&&", ",", "local.", "StringLiteral", "=", "/"),
            "<Type>": ("int", "string", "typedef", "function", "Identifier", "struct", "const", "boolean", "real"),
            "<Var Decl>": (
                "print(", "var", "HexLiteral", "StringLiteral", "procedure", "(", "false", "if", "typedef", "read(",
                "while", "const", "true", "function", "global.", "Identifier", "struct", "-", "FloatLiteral", "local.",
                "return", "OctLiteral", "DecLiteral"),
            "<Delimiter Const>": ("Identifier", "struct", "string", "const", "boolean", "real", "int"),
            "<Aux>": ("Identifier", "struct", "string", "var", "boolean", "real", "int"),
            "<Formal Parameter List Read>": ("read(", ","),
            "<If>": ("print(", "var", "HexLiteral", "false", "(", "if", "while", "true", "StringLiteral", "global.",
                     "Identifier", "-", "read(", "DecLiteral", "local.", "return", "OctLiteral", "FloatLiteral"),
            "<Return Statement>": (
                "print(", "var", "HexLiteral", "false", "(", "if", "while", "true", "StringLiteral", "global.",
                "Identifier", "-", "read(", "DecLiteral", "local.", "return", "OctLiteral", "FloatLiteral"),
            "<Decls>": ("Identifier", "struct", "$", "const", "var", "typedef", "function", "procedure"),
            "<Assignment_vector>": (
                "OctLiteral", ";", "=", "FloatLiteral", "[", "true", "HexLiteral", "global.", "Identifier",
                "StringLiteral",
                "-", ",", "local.", "false", "(", "DecLiteral"),
            "<Const Decl>": ("Identifier", "struct", "var", "typedef", "function", "procedure"),
            "<Else Procedure>": (
                "FloatLiteral", "var", "HexLiteral", "OctLiteral", "(", "if", "while", "true", "global.", "Identifier",
                "read(", "-", "print(", "local.", "false", "StringLiteral", "DecLiteral"),
            "<Body Procedure>": (
                "FloatLiteral", "var", "HexLiteral", "OctLiteral", "(", ")", "if", "StringLiteral", "while", "read(",
                "true", "DecLiteral", "global.", "Identifier", "procedure", "-", "false", "local.", "print(", "else",
                "start"),
            "<Extends>": ("Identifier", "boolean", "string", "int", "real", "struct"),
            "<Params>": ("Identifier", "procedure", "function"),
            "<While Procedure>": (
                "print(", "var", "HexLiteral", "StringLiteral", "(", "if", "while", "true", "global.", "Identifier",
                "read(", "-", "FloatLiteral", "local.", "false", "OctLiteral", "DecLiteral"),
            "<Term>": (
                "DecLiteral", "false", "true", "HexLiteral", "global.", "Identifier", "OctLiteral", "-", "FloatLiteral",
                "local.", "+", "(", "StringLiteral"),
            "<Mult Exp>": (
                "DecLiteral", "StringLiteral", "true", "HexLiteral", "global.", "Identifier", "OctLiteral", "-",
                "FloatLiteral", "local.", "+", "(", "false"),
            "<Program>": ("$"),
            "<Logical>": ("if", "while"),
            "<If Procedure>": (
                "print(", "var", "HexLiteral", "StringLiteral", "(", "if", "while", "true", "global.", "Identifier",
                "read(", "-", "FloatLiteral", "local.", "false", "OctLiteral", "DecLiteral"),
            "<Add Exp>": (
                "FloatLiteral", ">", "HexLiteral", "<", "OctLiteral", "<=", "==", ">=", "(", ";", "DecLiteral", "true",
                "false", "global.", "Identifier", "procedure", "-", ",", "local.", "StringLiteral", "!=", "print("),
            "<Assignment_vector_aux1>": (
                "DecLiteral", ";", "OctLiteral", "FloatLiteral", "false", "true", "=", "global.", "Identifier", "[",
                "-",
                ",", "local.", "StringLiteral", "(", "HexLiteral"),
            "<Assignment_vector_aux2>": (
                "DecLiteral", ";", "OctLiteral", "FloatLiteral", "false", "true", "=", "global.", "Identifier", "[",
                "-",
                ",", "local.", "StringLiteral", "(", "HexLiteral"),
            "<Typedef Decl>": ("Identifier", "struct", "typedef", "function", "procedure"),
            "<Decl>": ("Identifier", "struct", "typedef", "function", "procedure"),
            "<Print>": ("print(", "var", "HexLiteral", "false", "(", "if", "while", "true", "StringLiteral", "global.",
                        "Identifier", "-", "read(", "DecLiteral", "local.", "return", "OctLiteral", "FloatLiteral"),
            "<Then>": (
                "print(", "var", "HexLiteral", "false", "(", "if", "while", "true", "FloatLiteral", "global.",
                "Identifier",
                "OctLiteral", "-", "StringLiteral", "local.", "return", "read(", "DecLiteral"),
            "<Formal Parameter List>": ("Identifier", "procedure", "print("),
            "<Struct Decl>": ("Identifier", "struct", "typedef", "function", "procedure"),
            "<Assignment_matrix>": (
                "OctLiteral", ";", "=", "FloatLiteral", "[", "true", "HexLiteral", "global.", "Identifier",
                "StringLiteral",
                "-", ",", "local.", "false", "(", "DecLiteral"),
            "<Expression Value>": ("/", "*")
        }
        self.__production = {
            "<Start>": (("'start'", "'('", "')'", "'{'", "<Body Procedure>", "'}'", "<Decls>")),
            "<Proc Decl>": (("'procedure'", "Identifier", "'('", "<Params>", "')'", "'{'", "<Body Procedure>", "'}'"),
                            ("Identifier", "'('", "<Formal Parameter List>", "')'", "'{'", "<Body Procedure>", "'}'")),
            "<Param>": (("const", "<Type>", "Identifier"), ("<Type>", "Identifier")),
            "<Assignment_matrix_aux1>": (("<Assignment_vector_aux1>")),
            "<Value_assigned_vector>": (("<Value>", "','", "<Value_assigned_vector>"), ("<Value>")),
            "<Body Item>": (
                ("<Var Decl>"), ("<While>"), ("<If>"), ("<Read>"), ("<Print>"), ("<Assign>"), ("<Return Statement>")),
            "<Formal Parameter List Read>": (("Identifier"), ("<Formal Parameter List Read>", "','", "Identifier")),
            "<PrefixGlobalLocal>": (("'global.'"), ("'local.'")),
            "<Function Call>": (("Identifier", "'('", "<Formal Parameter List>", "')'")),
            "<Body Item Procedure>": (
                ("<Var Decl>"), ("<While Procedure>"), ("<If Procedure>"), ("<Read>"), ("<Print>"), ("<Assign>")),
            "<Body>": (("<Body Item>", "<Body>"), ("")),
            "<Relational>": (
                ("'>'", "<Exp>"), ("'<'", "<Exp>"), ("'<='", "<Exp>"), ("'>='", "<Exp>"), ("'=='", "<Exp>"),
                ("'!='", "<Exp>")),
            "<Conditional Expression>": (("<Boolean Literal>"), ("<Relational Expression>"), ("<Logical Expression>")),
            "<While>": (("'while'", "'('", "<Conditional Expression>", "')'", "'{'", "<Body>", "'}'")),
            "<Number>": (("DecLiteral"), ("OctLiteral"), ("HexLiteral"), ("FloatLiteral")),
            "<Base>": (("<Type>"), ("struct", "<Extends>", "'{'", "<VariablesList>", "'}'"), ("<Struct Decl>")),
            "<Assignment_matrix_aux2>": (("'='", "'{'", "'{'", "<Value_assigned_matrix>", "'}'", "<Dimensao_matrix2>")),
            "<Vector>": (("'['", "<Index>", "']'")),
            "<Index>": (("DecLiteral|", "OctLiteral|", "Identifier")),
            "<Value_assigned_matrix>": (("<Value>", "','", "<Value_assigned_matrix>"), ("<Value>")),
            "<Matrix>": (("'['", "<Index>", "']'", "<Vector>")),
            "<Struct Decl>": (("struct", "Identifier", "<Extends>", "'{'", "<VariablesList>", "'}'")),
            "<Conditional Operator>": (("'&&'"), ("'||'")),
            "<Formal Parameter List>": (("<Exp>"), ("<Exp>", "','", "<Formal Parameter List>"), ("")),
            "<Variable>": (("Identifier", "<Aux>")),
            "<Then Procedure>": (("')'", "'then'", "'{'", "<Body Procedure>", "'}'", "<Else Procedure>")),
            "<ConstList>": (("<Type>", "<Const>", "<ConstList>"), ("")),
            "<Function Declaration>": (
                ("'function'", "<Type>", "Identifier", "'('", "<Params>", "')'", "'{'", "<Body>", "'}'")),
            "<Const>": (("Identifier", "'='", "<Value>", "<Delimiter Const>")),
            "<Read>": (("read'('", "<Formal Parameter List Read>", "')'", "';'")),
            "<Dimensao_matrix2>": (("','", "'{'", "<Value_assigned_matrix>", "'}'", "'}'")),
            "<Relational Expression>": (("<Exp>", "<Relational>")),
            "<Delimiter Var>": (("','", "<Variable>"), ("';'")),
            "<Global Decl>": (
                ("<Const Decl>"), ("<Var Decl>"), ("<Const Decl>", "<Var Decl>"), ("<Var Decl>", "<Const Decl>"), ("")),
            "<Assign>": (
                ("<PrefixGlobalLocal>", "Identifier", "'='", "<Exp>", "';'"), ("Identifier", "'='", "<Exp>", "';'"),
                ("Identifier", "<Vector>", "<Assignment_vector>", "';'"),
                ("Identifier", "<Matrix>", "<Assignment_matrix>", "';'"), ("<Exp>", "';'")),
            "<VariablesList>": (("<Type>", "<Variable>", "<VariablesList>"), ("")),
            "<Logical Expression>": (("<Expression Value Logical>", "<Logical>"), ("<Logical Denied>")),
            "<Value>": (("<Number>"), ("<Boolean Literal>"), ("StringLiteral")),
            "<Exp>": (("<PrefixGlobalLocal>", "<Term>", "<Add Exp>"), ("<Term>", "<Add Exp>")),
            "<Expression Value>": (
                ("'-'", "<Expression Value>"), ("Identifier"), ("'('", "<Exp>", "')'"), ("<Number>"),
                ("<Boolean Literal>"),
                ("StringLiteral"), ("<Function Call>")),
            "<Type>": (("int"), ("real"), ("boolean"), ("string"), ("struct", "Identifier"), ("Identifier")),
            "<Mult Exp>": (("'*'", "<Term>"), ("'/'", "<Term>"), ("")),
            "<Delimiter Const>": (("','", "<Const>"), ("';'")),
            "<Term>": (("<Expression Value>", "<Mult Exp>")),
            "<Add Exp>": (("'+'", "<Exp>"), ("'-'", "<Exp>"), ("")),
            "<If>": (("'if'", "'('", "<Conditional Expression>", "<Then>")),
            "<Expression Value Logical>": (
                ("Identifier"), ("<Boolean Literal>"), ("StringLiteral"), ("<Function Call>"),
                ("<Relational Expression>")),
            "<Extends>": (("'extends'", "Identifier"), ("")),
            "<Assignment_vector>": (("<Assignment_vector_aux1>"), ("<Assignment_vector_aux2>"), ("")),
            "<Else>": (("'else'", "'{'", "<Body>", "'}'"), ("")),
            "<Logical Denied>": (("'!'", "Identifier"), ("'!'", "<Boolean Literal>"), ("'!'", "<Logical Expression>"),
                                 ("'!'", "<Relational Expression>")),
            "<Body Procedure>": (("<Body Item Procedure>", "<Body Procedure>"), ("")),
            "<Return Statement>": (("'return'", "';'"), ("'return'", "<Assign>")),
            "<Params>": (("<Param>", "','", "<Params>"), ("<Param>"), ("")),
            "<While Procedure>": (
                ("'while'", "'('", "<Conditional Expression>", "')'", "'{'", "<Body Procedure>", "'}'")),
            "<If Procedure>": (("'if'", "'('", "<Conditional Expression>", "<Then Procedure>")),
            "<Aux>": (("'='", "<Value>", "<Delimiter Var>"), ("<Delimiter Var>"),
                      ("<Vector>", "<Assignment_vector>", "<Delimiter Var>"),
                      ("<Matrix>", "<Assignment_matrix>", "<Delimiter Var>")),
            "<Program>": (("<Global Decl>", "<Decls>", "<Start>")),
            "<Logical>": (
                ("<Conditional Operator>", "<Expression Value Logical>"),
                ("<Conditional Operator>", "<Logical Denied>")),
            "<Const Decl>": (("'const'", "'{'", "<ConstList>", "'}'")),
            "<Then>": (("')'", "'then'", "'{'", "<Body>", "'}'", "<Else>")),
            "<Decls>": (("<Decl>", "<Decls>"), ("")),
            "<Assignment_vector_aux2>": (("'='", "'{'", "<Value_assigned_vector>", "'}'")),
            "<Typedef Decl>": (("typedef", "<Base>", "Identifier", "';'")),
            "<Decl>": (("<Function Declaration>"), ("<Proc Decl>"), ("<Struct Decl>"), ("<Typedef Decl>")),
            "<Print>": (("print'('", "<Formal Parameter List>", "')'", "';'")),
            "<Assignment_matrix>": (("<Assignment_matrix_aux1>"), ("<Assignment_matrix_aux2>"), ("")),
            "<Var Decl>": (("'var'", "'{'", "<VariablesList>", "'}'")),
            "<Boolean Literal>": (("'true'"), ("'false'")),
            "<Assignment_vector_aux1>": (("'='", "<Value>")),
            "<Else Procedure>": (("'else'", "'{'", "<Body Procedure>", "'}'"), (""))
        }

    def get_productions(self) -> {tuple[str]}:
        return self.__production

    def get_first(self) -> dict[tuple[str]]:
        return self.__first

    def get_follow(self) -> dict[tuple[str]]:
        return self.__follow
