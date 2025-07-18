

class AstPrinter: 
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        print("in main", method_name)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return f"<Unknown:{type(node).__name__}>"
    
    def visit_Program(self, node):
        return "\n\n".join(self.visit(item) for item in node.items)

    def visit_FunctionDef(self, node):
        print("in funcdef")
        header = "unsafe " if node.unsafe else ""
        header += f"fn {node.identifier}("
        header += self.visit(node.params) + ")"
        if node.return_type:
            header += f" -> {self.visit(node.return_type)}"
        body = self.visit(node.body)
        return f"{header} {body}"

    def visit_FunctionParamList(self, node):
        return ", ".join(self.visit(param) for param in node.params)

    def visit_Param(self, node):
        mut = "mut " if node.mutable else ""
        return f"{mut}{node.name}: {self.visit(node.typ)}"

    def visit_TypeName(self, node):
        return node.name  # assuming TypeName just wraps a string type name

    def visit_Block(self, node):
        stmts = "\n".join("    " + self.visit(stmt) for stmt in node.stmts)
        return "{\n" + stmts + "\n}"

    def visit_LetStmt(self, node):
        if not node.is_destructuring():
            var = node.var_defs[0]
            val = self.visit(node.values[0])
            return f"let {self.visit(var)} = {val};"

        vars_str = ", ".join(self.visit(v) for v in node.var_defs)
        vals_str = ", ".join(self.visit(v) for v in node.values)
        return f"let ({vars_str}) = ({vals_str});"
    
    def visit_VarDef(self, node):
        mut = "mut " if getattr(node, "is_mut", False) else ""
        return f"{mut}{node.name}: {self.visit(node.type)}"  # or just node.name if no type

    def visit_Literal(self, node):
        return str(node.value)

    def visit_Identifier(self, node):
        return node.name

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

    def visit_IfStmt(self, node):
        cond = self.visit(node.condition)
        then = self.visit(node.then_branch)
        result = f"if ({cond}) {then}"
        if node.else_branch:
            result += f" else {self.visit(node.else_branch)}"
        return result

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
    
    def visit_Type(self, node):
        print("********")

    def visit_BoolType(self, node):
        return "bool"

    def visit_IntType(self, node):
        return "i32"

    def visit_StringType(self, node):
        return "String"

    def visit_FloatType(self, node):
        return "f32"

    def visit_str(self, node):
        return node