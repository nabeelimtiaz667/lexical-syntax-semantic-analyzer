from c_lexer import lexer
from c_parser import parser
from semantic_analyzer import SemanticAnalyzer

file_path = "sourceCode-C-lang.txt"

with open(file_path, "r") as f:
    content = f.read()

lexer.input(content)
ast_root = parser.parse(content, lexer=lexer)

tokens_list = []

# print("Generated Tokens:")
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     tokens_list.append(tok)
#     print(
#         f"Type: {tok.type}, Value: {tok.value}, Line: {tok.lineno}, Position: {tok.lexpos}"
#     )

if ast_root:
    print("PARSING SUCCESSFUL\n")

    print("\nIn Order Traversal:")
    nodes = ast_root.pretty()
    for n in nodes:
        print(n, end="")
else:
    print("Parsing failed")

print("\nSEMANTIC ANALYSIS")
SemanticAnalyzer(ast_root).analyze()
