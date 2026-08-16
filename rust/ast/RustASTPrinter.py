from rust.ast.ASTNode import CloneableASTNode
from rust.ast.Expression import BinaryExpression, Expression, FieldAccessExpr, FunctionCallExpression, ArrayLiteral, \
    BorrowExpression, TypePath, RangeExpression, StructLiteral, CastExpression, TypedName
from rust.ast.Func import FunctionParamList, Param
from rust.ast.Program import Program
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.Struct import StructField
from rust.ast.TopLevel import *
from rust.ast.Type import ExternalType, UnknownType
from rust.ast.Statement import WhileStmt


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
        return "\n\n".join(self.visit(child) for child in ctx.getChildren())

    def visitExternBlock(self, ctx: ExternBlock):
        re = "extern \"" + f"{ctx.name()}"
        re = re.join(str(child.accept(self)) + " ;" for child in ctx.items())
        return f"{re}"

    def visitExternFunctionDecl(self, ctx: ExternFunctionDecl):
        re = "fn "
        if ctx.visibility is not None:
            re += "pub "
        re += f"{ctx.name}" +"("

        for i in range(len(ctx.params)):
            re += f"{ctx.params[i].accept(self)}"
            if i < len(ctx.params) - 1:
                re += ","
        re += ")"
        if ctx.return_type is not None:
            re += f" -> {ctx.return_type.accept(self)}" +" ;"
        return f"{re}"

    def visitFunctionDef(self, ctx: FunctionDef):
        header = "unsafe " if ctx.isUnsafe else ""
        header += f"fn {ctx.identifier}("
        # Concatenate the items of the param to the string
        params_list = ctx.params
        param_str = ','.join(str(param.accept(self)) for param in params_list)
        header += param_str + ")" # .accept(self)
        if ctx.return_type:
            header += f" -> {ctx.return_type.accept(self)}"
        body = ctx.body.accept(self)
        return f"{header} {body}"

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        # print("callee" + node.callee())
        result = self.visit(node.caller()) # This part
        if node.callee() is not None:
            result += "." + self.visit(node.callee())
        result += "("
        for i in range(len(node.args())):
            result += self.visit(node.args()[i]) # This part
            if i < len(node.args()) - 1:
                result += ","
        result += ")"
        return f"{result}"

    def visitFunctionParamList(self, ctx: FunctionParamList):
        return ", ".join(self.visit(param) for param in ctx.params)

    def visitParam(self, ctx: Param):
        mut = "mut " if ctx.isMutable else ""
        type = ctx.type.accept(self)
        return f"{mut}{ctx.name}: {type}"

    def visitTypeName(self, node):
        return node.name  # assuming TypeName just wraps a string type name

    def visitBlock(self, node):
        stmts = "\n".join("    " + str(self.visit(stmt)) for stmt in node.statements())
        return "{\n" + stmts + "\n}"

    def visitLetStmt(self, node):
        if not node.is_destructuring():
            var = node.var_defs[0]
            val = self.visit(node.values[0])
            return f"let {self.visit(var)} = {val};"

        vars_str = ", ".join(self.visit(v) for v in node.var_defs)
        vals_str = ", ".join(self.visit(v) for v in node.values)
        return f"let ({vars_str}) = ({vals_str});"

    def visitWhileStmt(self, node: WhileStmt):
        condition = self.visit(node.condition)
        # print(node.body)
        body = self.visit(node.body)
        return f"while ({condition}) {body}"

    def visitVarDef(self, node):
        mut = "mut " if getattr(node, "is_mut", False) else ""
        if node.type() is not None:
            return f"{mut}{node.name()}: {self.visit(node.type())}"  # or just node.name if no type
        else:
            return f"{mut}{node.name()}: None" # {self.visit(node.vardef_type)}

    def visitLiteral(self, node):
        if isinstance(node, ArrayLiteral):
            re = "["
            for i in range(len(node.value())):
                re += self.visit(node.value()[i])
                if i < len(node.value()) - 1:
                    re += ","
            re += "]"
        else:
            re = str(node.value())
        return f"{re}"

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

    # def visitFieldAccessExpr(self, node: FieldAccessExpr):
    #     re = "."+self.visit(node.receiver()) #.join(self.visit(nv) for nv in node.receiver())
    #     re += "."+self.visit(node.next())
    #     return f"#[{re}]"

    def visitRangeExpression(self, node: RangeExpression):
        re = ""
        re += self.visit(node.initial())
        re += ".."
        re += self.visit(node.last())
        return f"{re}"

    def visitBorrowExpression(self, node: BorrowExpression):
        if node.is_mutable():
            re = "mut "
        else:
            re = ""
        v = self.visit(node.expression())
        return f"{re}" + "&" + f"{v}"

    def visitUseDecl(self, ctx: UseDecl):
        re = ""
        for v in ctx.paths:
            re += self.visit(v)
        return f"{re}" + ";"

    def visitTypePath(self, node: TypePath):
        re = ""
        if node.hasColumn():
            re += "::"

        for v in node.types():
            re += f"{v}"

        return f"{re}"

    def visitTypedName(self, node: TypedName):
        re = f"{self.visit(node.types())}"
        re += f"{self.visit(node.name())}"
        return f"{re}"


    def visitCastExpression(self, ctx: CastExpression):
        re = f"{ctx.expression().accept(self)}"
        for child in ctx.type():
            re = f"{child.accept(self)}"
            re += ","
        return f"{re}"


    def visitBinaryExpression(self, node: BinaryExpression):
        op = node.op()
        # left = self.visit(node.left())
        # right = self.visit(node.right())
        left = node.left()
        if isinstance(left, Expression):
            left = self.visit(left)
        right = node.right()
        if isinstance(right, Expression):
            right = self.visit(right)
        return f"({left} {op} {right})"

    def visitStructDef(self, node : StructADef):
        if node.visibility is not None:
            re = "pub "
        else:
            re = ""

        re += "struct " + f"{node.name}" + " {"
        for f in node.fields:
            re += f"{self.visit(f)}"
            re += ", "
        re += " }"
        return f"{re}"

    def visitStructField(self, node: StructField):
        if node.visibility is not None:
            re = "pub "
        else:
            re = ""

        re += f"{node.name}"
        re += node.dtype.accept(self)
        return f"{re}"

    def visitStructLiteral(self, node : StructLiteral):
        fields = ", ".join(f"{f.name}: {self.visit(f.value)}" for f in node.fields)
        return f"{node.type_name} {{ {fields} }}"

    def visitUnaryExpr(self, node):
        return f"{node.op()}{self.visit(node.expression())}"

    def visitAttribute(self, node):
        #if node.args:
        #    args_str = ", ".join(self.visit(arg) for arg in node.args)
        #    return f"#[{node.name}({args_str})]"
        return f"#[{node.name}]"

    def visitFieldAccessExpr(self, node):
        receiver = self.visit(node.receiver())
        return f"{receiver}.{self.visit(node.next())}"

    def visitBoolType(self, node):
        return "bool"

    def visitSignedIntType(self, node):
        return "i32"

    def visitStringType(self, node):
        return "String"

    def visitFloatType(self, node):
        return "f32"

    def visitExternalType(self, node: ExternalType):
        left = node.ctype()
        right = node.ptype()
        return f"{left} + :: + {right}"

    def visitUnknownType(self, node: UnknownType):
        return f"{node.ptype()}"

    def visitStr(self, node):
        return node