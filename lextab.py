# lextab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('AND', 'ANDAND', 'CHAR', 'COMMA', 'DIVIDE', 'DOT', 'ELSE', 'EQEQ', 'EQUALS', 'FLOAT', 'FOR', 'GE', 'GT', 'HASH', 'ID', 'IF', 'INCLUDE', 'INT', 'LBRACE', 'LBRACKET', 'LE', 'LPAREN', 'LT', 'MAIN', 'MINUS', 'MODULO', 'NEQ', 'NUMBER', 'PLUS', 'RBRACE', 'RBRACKET', 'RETURN', 'RPAREN', 'SEMICOLON', 'STRING_LITERAL', 'TIMES', 'VOID', 'WHILE'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_ANDAND>\\&\\&)|(?P<t_AND>\\&)|(?P<t_STRING_LITERAL>"([^\\\\]|\\\\.)*?")|(?P<t_NUMBER>\\d+)|(?P<t_ID>[A-Za-z_][A-Za-z0-9_]*)|(?P<t_COMMENT>/\\*[\\s\\S]*?\\*/)|(?P<t_LINE_COMMENT>//.*)|(?P<t_newline>\\n+)|(?P<t_EQEQ>==)|(?P<t_NEQ>!=)|(?P<t_LE><=)|(?P<t_GE>>=)|(?P<t_PLUS>\\+)|(?P<t_TIMES>\\*)|(?P<t_LPAREN>\\()|(?P<t_RPAREN>\\))|(?P<t_LBRACE>\\{)|(?P<t_RBRACE>\\})|(?P<t_LBRACKET>\\[)|(?P<t_RBRACKET>\\])|(?P<t_DOT>\\.)|(?P<t_HASH>\\#)|(?P<t_LT><)|(?P<t_GT>>)|(?P<t_EQUALS>=)|(?P<t_MINUS>-)|(?P<t_DIVIDE>/)|(?P<t_MODULO>%)|(?P<t_SEMICOLON>;)|(?P<t_COMMA>,)', [None, ('t_ANDAND', 'ANDAND'), ('t_AND', 'AND'), ('t_STRING_LITERAL', 'STRING_LITERAL'), None, ('t_NUMBER', 'NUMBER'), ('t_ID', 'ID'), ('t_COMMENT', 'COMMENT'), ('t_LINE_COMMENT', 'LINE_COMMENT'), ('t_newline', 'newline'), (None, 'EQEQ'), (None, 'NEQ'), (None, 'LE'), (None, 'GE'), (None, 'PLUS'), (None, 'TIMES'), (None, 'LPAREN'), (None, 'RPAREN'), (None, 'LBRACE'), (None, 'RBRACE'), (None, 'LBRACKET'), (None, 'RBRACKET'), (None, 'DOT'), (None, 'HASH'), (None, 'LT'), (None, 'GT'), (None, 'EQUALS'), (None, 'MINUS'), (None, 'DIVIDE'), (None, 'MODULO'), (None, 'SEMICOLON'), (None, 'COMMA')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
