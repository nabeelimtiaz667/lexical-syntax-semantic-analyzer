import ply.lex as lex

# List of C keywords
reserved = {
    "if": "IF",
    "else": "ELSE",
    "for": "FOR",
    "while": "WHILE",
    "int": "INT",
    "float": "FLOAT",
    "char": "CHAR",
    "return": "RETURN",
    "void": "VOID",
    "main": "MAIN",
    "include": "INCLUDE",
    # 'stdio': 'STDIO',
    # 'string': 'STRING_KEYWORD'
}

tokens = [
    "ID",
    "NUMBER",
    "STRING_LITERAL",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULO",
    "EQUALS",
    "EQEQ",
    "NEQ",
    "LT",
    "LE",
    "GT",
    "GE",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "SEMICOLON",
    "COMMA",
    "DOT",
    "HASH",
    "AND",
    "ANDAND",
] + list(reserved.values())

# Operators
t_EQEQ = r"=="
t_NEQ = r"!="
t_LE = r"<="
t_GE = r">="
t_LT = r"<"
t_GT = r">"
t_EQUALS = r"="

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MODULO = r"%"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_SEMICOLON = r";"
t_COMMA = r","
t_DOT = r"\."
t_HASH = r"\#"


def t_ANDAND(t):
    r"\&\&"
    return t


def t_AND(t):
    r"\&"
    return t


def t_STRING_LITERAL(t):
    r'"([^\\]|\\.)*?"'
    t.value = t.value[1:-1]
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_COMMENT(t):
    r"/\*[\s\S]*?\*/"
    pass


def t_LINE_COMMENT(t):
    r"//.*"
    pass


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = " \t"


def t_error(t):
    raise Exception(f"Lexical error: '{t.value[0]}' at line {t.lexer.lineno}")


lexer = lex.lex(optimize=True)
