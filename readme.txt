Required following libs:
pip install ply

OVERVIEW: 
1- Lexical Analysis: Tokenized the code and created lexems, constructed a Context-Free Grammar (CFG) based on it. (c_lexer.py)
2- Syntax Analysis: Parsed the incoming CFG through LALR Grammar. It produced an Abstract Syntax Tree (AST) ready for semantic analysis.
3- Semantic Analysis: Analyzed the AST for:
    a. Type Compatibility
    b. Scope Resolution
    c. Function Signature Validation
    Produced block-level Symbol Table.

INSTRCUTION:
Run main.py