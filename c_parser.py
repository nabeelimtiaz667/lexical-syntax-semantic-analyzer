import ply.yacc as yacc
from c_lexer import tokens

precedence = (
    ("left", "EQEQ", "NEQ"),
    ("left", "LT", "LE", "GT", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MODULO"),
    ("right", "UMINUS"),
)


class ASTNode:
    def __init__(self, nodetype, children=None, **attrs):
        self.nodetype = nodetype
        self.children = children or []
        self.attrs = attrs

    def __repr__(self):
        return f"{self.nodetype}({self.attrs})"

    def pretty(self, level=0):
        indent = "  " * level
        s = f"{indent}{self.nodetype} {self.attrs}\n"
        for c in self.children:
            if isinstance(c, ASTNode):
                s += c.pretty(level + 1)
            else:
                s += f"{indent}  {c}\n"
        return s


def p_program(p):
    """program : headers main_function"""
    p[0] = ASTNode("Program", children=[p[1], p[2]])


def p_headers(p):
    """headers : headers header
    | header"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_header(p):
    """header : HASH INCLUDE LT ID DOT ID GT"""
    p[0] = ASTNode("Header", name=f"{p[4]}.{p[6]}")


def p_main_function(p):
    """main_function : type MAIN LPAREN RPAREN compound_stmt"""
    p[0] = ASTNode(
        "Function",
        children=[p[5]],
        name="main",
        return_type=p[1],
    )


def p_type(p):
    """type : INT
    | FLOAT
    | CHAR
    | VOID"""
    p[0] = p[1]


def p_compound_stmt(p):
    """compound_stmt : LBRACE stmt_list RBRACE"""
    p[0] = ASTNode("Block", children=p[2])


def p_stmt_list(p):
    """stmt_list : stmt_list statement
    | statement"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    """statement : declaration SEMICOLON
    | assignment SEMICOLON
    | if_stmt
    | for_stmt
    | return_stmt
    | func_call SEMICOLON
    | compound_stmt
    | SEMICOLON"""
    p[0] = p[1] if p[1] != ";" else ASTNode("Empty")


def p_declaration(p):
    """declaration : type declarator_list"""
    p[0] = ASTNode("VarDecl", children=p[2], datatype=p[1])


def p_declarator_list(p):
    """declarator_list : declarator_list COMMA declarator
    | declarator"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_declarator(p):
    """declarator : ID
    | ID EQUALS expression"""
    if len(p) == 2:
        p[0] = ASTNode("Declarator", name=p[1])
    else:
        p[0] = ASTNode("Declarator", name=p[1], init=p[3])


def p_assignment(p):
    """assignment : ID EQUALS expression"""
    p[0] = ASTNode("Assign", children=[ASTNode("Identifier", name=p[1]), p[3]])


def p_if_stmt(p):
    """if_stmt : IF LPAREN expression RPAREN statement
    | IF LPAREN expression RPAREN statement ELSE statement"""
    if len(p) == 6:
        p[0] = ASTNode("If", children=[p[3], p[5]])
    else:
        p[0] = ASTNode("If", children=[p[3], p[5], p[7]])


def p_for_stmt(p):
    """for_stmt : FOR LPAREN for_init SEMICOLON expression SEMICOLON for_update RPAREN statement"""
    p[0] = ASTNode("For", children=[p[3], p[5], p[7], p[9]])


def p_for_init(p):
    """for_init : declaration
    | assignment
    | empty"""
    p[0] = p[1]


def p_for_update(p):
    """for_update : assignment
    | ID PLUS PLUS
    | empty"""
    if len(p) == 4:
        p[0] = ASTNode(
            "Assign",
            children=[
                ASTNode("Identifier", name=p[1]),
                ASTNode(
                    "BinOp",
                    operator="+",
                    children=[
                        ASTNode("Identifier", name=p[1]),
                        ASTNode("Literal", value=1, datatype="int"),
                    ],
                ),
            ],
        )
    else:
        p[0] = p[1]


def p_return_stmt(p):
    """return_stmt : RETURN expression SEMICOLON"""
    p[0] = ASTNode("Return", children=[p[2]])


def p_func_call(p):
    """func_call : ID LPAREN arg_list RPAREN"""
    p[0] = ASTNode("Call", children=p[3], name=p[1])


def p_arg_list(p):
    """arg_list : arg_list COMMA expression
    | expression
    | empty"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1].nodetype != "Empty":
        p[0] = [p[1]]
    else:
        p[0] = []


def p_expression(p):
    """expression : relational_expression"""
    p[0] = p[1]


def p_relational_expression(p):
    """relational_expression : additive_expression
    | additive_expression LT additive_expression
    | additive_expression LE additive_expression
    | additive_expression GT additive_expression
    | additive_expression GE additive_expression
    | additive_expression EQEQ additive_expression
    | additive_expression NEQ additive_expression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("BinOp", children=[p[1], p[3]], operator=p[2])


def p_additive_expression(p):
    """additive_expression : additive_expression PLUS term
    | additive_expression MINUS term
    | term"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("BinOp", children=[p[1], p[3]], operator=p[2])


def p_term(p):
    """term : term TIMES factor
    | term DIVIDE factor
    | term MODULO factor
    | factor"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("BinOp", children=[p[1], p[3]], operator=p[2])


def p_factor(p):
    """factor : NUMBER
    | STRING_LITERAL
    | ID
    | LPAREN expression RPAREN
    | MINUS factor %prec UMINUS"""
    if len(p) == 2:
        tok_type = p.slice[1].type

        if tok_type == "NUMBER":
            p[0] = ASTNode("Literal", value=p[1], datatype="int")

        elif tok_type == "STRING_LITERAL":
            p[0] = ASTNode("Literal", value=p[1], datatype="string")

        elif tok_type == "ID":
            p[0] = ASTNode("Identifier", name=p[1])

    elif len(p) == 3:
        p[0] = ASTNode("UnaryOp", children=[p[2]], operator="-")

    else:
        p[0] = p[2]


def p_factor_address(p):
    "factor : AND ID"
    p[0] = ASTNode("AddressOf", children=[ASTNode("Identifier", name=p[2])])


def p_empty(p):
    "empty :"
    p[0] = ASTNode("Empty")


def p_error(p):
    if p:
        raise Exception(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        raise Exception("Syntax error at EOF")


parser = yacc.yacc()
