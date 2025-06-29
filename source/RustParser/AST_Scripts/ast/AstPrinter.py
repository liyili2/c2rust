

class AstPrinter:
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return f"<Unknown:{type(node).__name__}>"
    
    def visit_Program(self, node):
        return "\n".join(self.visit(item) for item in node.items)

    def visit_LetStmt(self, node):
        decl = self.visit(node.declared_type) if node.declared_type else ""
        val = self.visit(node.value)
        return f"let {node.identifier} : {decl} = {val};"

    def visit_AssignStmt(self, node):
        target = self.visit(node.target)
        value = self.visit(node.value)
        return f"{target} = {value};"

    def visit_ReturnStmt(self, node):
        if node.value:
            return f"return {self.visit(node.value)};"
        return "return;"

    def visit_CallStmt(self, node):
        return self.visit(node.call) + ";"

    def visit_Block(self, node):
        stmts = "\n".join(self.visit(s) for s in node.stmts)
        return f"{{\n{stmts}\n}}"

    def visit_IfStmt(self, node):
        cond = self.visit(node.condition)
        then = self.visit(node.then_branch)
        result = f"if ({cond}) {then}"
        if node.else_branch:
            result += f" else {self.visit(node.else_branch)}"
        return result

    def visit_Identifier(self, node):
        return node.name

    def visit_Literal(self, node):
        return str(node.value)

    def visit_BinaryExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.op} {right})"

    def visit_StructLiteral(self, node):
        fields = ", ".join(f"{f.name}: {self.visit(f.value)}" for f in node.fields)
        return f"{node.type_name} {{ {fields} }}"

    def visit_UnaryExpr(self, node):
        return f"{node.op}{self.visit(node.expr)}"

    def visit_CallExpr(self, node):
        args = ", ".join(self.visit(arg) for arg in node.args)
        return f"{self.visit(node.func)}({args})"

    def visit_Attribute(self, node):
        if node.args:
            args_str = ", ".join(self.visit(arg) for arg in node.args)
            return f"#[{node.name}({args_str})]"
        return f"#[{node.name}]"

    def visit_FieldAccessExpr(self, node):
        receiver = self.visit(node.receiver)
        return f"{receiver}.{node.name}"
