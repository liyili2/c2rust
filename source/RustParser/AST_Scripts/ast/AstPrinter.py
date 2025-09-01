

class AstPrinter: 
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        print("in main", method_name)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return f"<Unknown:{type(node).__name__}>"
    
    def visitProgram(self, node):
        return "\n\n".join(self.visit(item) for item in node.items)

    def visitFunctionDef(self, node):
        print("in funcdef")
        header = "unsafe " if node.unsafe else ""
        header += f"fn {node.identifier}("
        header += self.visit(node.params) + ")"
        if node.return_type:
            header += f" -> {self.visit(node.return_type)}"
        body = self.visit(node.body)
        return f"{header} {body}"

    def visitFunctionParamList(self, node):
        return ", ".join(self.visit(param) for param in node.params)

    def visitParam(self, node):
        mut = "mut " if node.mutable else ""
        return f"{mut}{node.name}: {self.visit(node.typ)}"

    def visitTypeName(self, node):
        return node.name  # assuming TypeName just wraps a string type name

    def visitBlock(self, node):
        stmts = "\n".join("    " + self.visit(stmt) for stmt in node.stmts)
        return "{\n" + stmts + "\n}"

    def visitLetStmt(self, node):
        if not node.is_destructuring():
            var = node.var_defs[0]
            val = self.visit(node.values[0])
            return f"let {self.visit(var)} = {val};"

        vars_str = ", ".join(self.visit(v) for v in node.var_defs)
        vals_str = ", ".join(self.visit(v) for v in node.values)
        return f"let ({vars_str}) = ({vals_str});"
    
    def visitVarDef(self, node):
        mut = "mut " if getattr(node, "is_mut", False) else ""
        return f"{mut}{node.name}: {self.visit(node.type)}"  # or just node.name if no type

    def visitLiteral(self, node):
        return str(node.value)

    def visitIdentifier(self, node):
        return node.name

    def visitAssignStmt(self, node):
        target = self.visit(node.target)
        value = self.visit(node.value)
        return f"{target} = {value};"

    def visitReturnStmt(self, node):
        if node.value:
            return f"return {self.visit(node.value)};"
        return "return;"

    def visitCallStmt(self, node):
        return self.visit(node.call) + ";"

    def visitIfStmt(self, node):
        cond = self.visit(node.condition)
        then = self.visit(node.then_branch)
        result = f"if ({cond}) {then}"
        if node.else_branch:
            result += f" else {self.visit(node.else_branch)}"
        return result

    def visitBinaryExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.op} {right})"

    def visitStructLiteral(self, node):
        fields = ", ".join(f"{f.name}: {self.visit(f.value)}" for f in node.fields)
        return f"{node.type_name} {{ {fields} }}"

    def visitUnaryExpr(self, node):
        return f"{node.op}{self.visit(node.expr)}"

    def visitCallExpr(self, node):
        args = ", ".join(self.visit(arg) for arg in node.args)
        return f"{self.visit(node.func)}({args})"

    def visitAttribute(self, node):
        if node.args:
            args_str = ", ".join(self.visit(arg) for arg in node.args)
            return f"#[{node.name}({args_str})]"
        return f"#[{node.name}]"

    def visitFieldAccessExpr(self, node):
        receiver = self.visit(node.receiver)
        return f"{receiver}.{node.name}"
    
    def visitType(self, node):
        print("********")

    def visitBoolType(self, node):
        return "bool"

    def visitIntType(self, node):
        return "i32"

    def visitStringType(self, node):
        return "String"

    def visitFloatType(self, node):
        return "f32"

    def visitStr(self, node):
        return node