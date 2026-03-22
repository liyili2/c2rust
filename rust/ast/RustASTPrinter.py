from rust.ast.Func import FunctionParamList, Param
from rust.ast.Program import Program
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.TopLevel import FunctionDef


class RustASTPrinter(RustASTVisitor):

    # def visit(self, node):
    #     method_name = f"visit_{type(node).__name__}"
    #     print("in main", method_name)
    #     visitor = getattr(self, method_name, self.generic_visit)
    #     return visitor(node)
    #
    # def generic_visit(self, node):
    #     return f"<Unknown:{type(node).__name__}>"
    
    def visitProgram(self, ctx: Program):
        return "\n\n".join(child.accept(self) for child in ctx.getChildren())

    def visitFunctionDef(self, ctx: FunctionDef):
        header = "unsafe " if ctx.isUnsafe else ""
        header += f"fn {ctx.identifier}("
        header += ctx.params.accept(self) + ")"
        if ctx.return_type:
            header += f" -> {ctx.return_type.accept(self)}"
        body = ctx.body.accept(self)
        return f"{header} {body}"

    def visitFunctionParamList(self, ctx: FunctionParamList):
        return ", ".join(self.visit(param) for param in ctx.params)

    def visitParam(self, ctx: Param):
        mut = "mut " if ctx.isMutable else ""
        return f"{mut}{ctx.declarationInfo.name}: {ctx.declarationInfo.dtype}"

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
        return f"{mut}{node.name}: {self.visit(node.dtype)}"  # or just node.name if no type

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

    def visitBinaryExpression(self, node):
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