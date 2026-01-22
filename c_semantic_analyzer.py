class SemanticError(Exception):
    pass


class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def declare(self, name, datatype):
        if name in self.symbols:
            raise SemanticError(f"Redeclaration of variable '{name}'")
        self.symbols[name] = datatype

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        raise SemanticError(f"Undeclared identifier '{name}'")


class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []

        self.functions = {
            "printf": {
                "params": ["string"],
                "return": "int",
            },
            "scanf": {
                "params": ["string", "int*"],
                "return": "int",
            },
            "main": {
                "params": [],
                "return": "int",
            },
        }

    def analyze(self):
        try:
            self.visit(self.ast, SymbolTable())
        except SemanticError as e:
            self.errors.append(str(e))

        if self.errors:
            print("❌ Semantic Errors:")
            for err in self.errors:
                print("  -", err)
        else:
            print("✅ Semantic analysis successful. No errors found.")

    def visit(self, node, scope):
        method = getattr(self, f"visit_{node.nodetype}", self.generic_visit)
        return method(node, scope)

    def generic_visit(self, node, scope):
        for child in node.children:
            if hasattr(child, "nodetype"):
                self.visit(child, scope)

    def visit_Program(self, node, scope):
        # headers ignored semantically
        function = node.children[1]
        self.visit(function, scope)

    def visit_Function(self, node, scope):
        name = node.attrs["name"]
        return_type = node.attrs["return_type"]

        if name not in self.functions:
            raise SemanticError(f"Undefined function '{name}'")

        if self.functions[name]["return"] != return_type:
            raise SemanticError(f"Function '{name}' return type mismatch")

        func_scope = SymbolTable(scope)
        self.visit(node.children[0], func_scope)

    def visit_Block(self, node, scope):
        block_scope = SymbolTable(scope)
        for stmt in node.children:
            self.visit(stmt, block_scope)

    def visit_VarDecl(self, node, scope):
        datatype = node.attrs["datatype"]

        for declarator in node.children:
            name = declarator.attrs["name"]
            scope.declare(name, datatype)

            if "init" in declarator.attrs:
                init_type = self.eval_expr(declarator.attrs["init"], scope)
                if init_type != datatype:
                    raise SemanticError(f"Type mismatch in initialization of '{name}'")

    def visit_Assign(self, node, scope):
        lhs = node.children[0]
        rhs = node.children[1]

        lhs_type = scope.lookup(lhs.attrs["name"])
        rhs_type = self.eval_expr(rhs, scope)

        if lhs_type != rhs_type:
            raise SemanticError(f"Type mismatch in assignment to '{lhs.attrs['name']}'")

    def visit_If(self, node, scope):
        condition = node.children[0]
        cond_type = self.eval_expr(condition, scope)

        if cond_type != "int":
            raise SemanticError("Condition expression must be int")

        self.visit(node.children[1], scope)

        if len(node.children) == 3:
            self.visit(node.children[2], scope)

    def visit_For(self, node, scope):
        loop_scope = SymbolTable(scope)

        init, cond, update, body = node.children

        if init.nodetype != "Empty":
            self.visit(init, loop_scope)

        if cond.nodetype != "Empty":
            cond_type = self.eval_expr(cond, loop_scope)
            if cond_type != "int":
                raise SemanticError("For-loop condition must be int")

        if update.nodetype != "Empty":
            self.visit(update, loop_scope)

        self.visit(body, loop_scope)

    def visit_Return(self, node, scope):
        return self.eval_expr(node.children[0], scope)

    def visit_Call(self, node, scope):
        name = node.attrs["name"]

        if name not in self.functions:
            raise SemanticError(f"Call to undefined function '{name}'")

        expected = self.functions[name]["params"]
        args = node.children

        if len(args) != len(expected):
            raise SemanticError(f"Argument count mismatch in call to '{name}'")

        for arg, exp_type in zip(args, expected):
            actual = self.eval_expr(arg, scope)
            if exp_type == "int*" and actual != "int":
                raise SemanticError("scanf requires address of int")
            elif exp_type != "int*" and actual != exp_type:
                raise SemanticError(f"Argument type mismatch in call to '{name}'")

    def eval_expr(self, node, scope):
        if node.nodetype == "Literal":
            return node.attrs["datatype"]

        if node.nodetype == "Identifier":
            return scope.lookup(node.attrs["name"])

        if node.nodetype == "BinOp":
            left = self.eval_expr(node.children[0], scope)
            right = self.eval_expr(node.children[1], scope)

            if left != right:
                raise SemanticError("Binary operand type mismatch")
            return "int"

        if node.nodetype == "UnaryOp":
            return self.eval_expr(node.children[0], scope)

        if node.nodetype == "Call":
            return self.functions[node.attrs["name"]]["return"]

        if node.nodetype == "AddressOf":
            base = node.children[0]
            base_type = scope.lookup(base.attrs["name"])
            return base_type  # treated as int*

        raise SemanticError(f"Unknown expression type '{node.nodetype}'")
