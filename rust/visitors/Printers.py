from rust.nodes.Expression import BinaryExpression, Expression, FieldAccessExpr, FunctionCallExpression, ArrayLiteral, \
    BorrowExpression, TypePath, RangeExpression, StructLiteral, CastExpression, TypedName
from rust.nodes.Func import FunctionParamList, Param
from rust.nodes.Struct import StructField
from rust.nodes.TopLevel import *
from rust.nodes.Type import ExternalType, UnknownType
from rust.visitors.Base import RustASTVisitor


class RustASTPrinter(RustASTVisitor):
    
    def visitProgram(self, node: Program):
        i = 0
        exps = []
        while node.exp(i) is not None:
            exps.append(node.exp(i).accept(self))
            i += 1

        return "\n\n".join(exps)

    def visitExternBlock(self, node: ExternBlock):
        re = "extern \"" + f"{node.name()}"

        i = 0
        exps = []
        while node.program().exp(i) is not None:
            exps.append(node.program().exp(i).accept(self))
            i += 1

        re = re.join(str(exp) + " ;" for exp in exps)
        return f"{re}"

    def visitExternFunctionDeclaration(self, node: ExternFunctionDeclaration):
        re = "fn "
        if node.visibility() is not None:
            re += "pub "
        re += f"{node.name()}" + "("

        for i in range(len(node.params())):
            re += f"{node.params()[i].accept(self)}"
            if i < len(node.params()) - 1:
                re += ","
        re += ")"
        if node.return_type() is not None:
            re += f" -> {node.return_type().accept(self)}" + " ;"
        return f"{re}"

    def visitFunctionDefinition(self, node: FunctionDefinition):
        header = "unsafe " if node.is_unsafe() else ""
        header += f"fn {node.identifier()}("
        # Concatenate the items of the param to the string
        params_list = node.params()
        param_str = ','.join(str(param.accept(self)) for param in params_list)
        header += param_str + ")"
        if node.return_type():
            header += f" -> {node.return_type().accept(self)}"
        body = node.body().accept(self)
        return f"{header} {body}"

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        result = self.visit(node.caller())
        if node.callee() is not None:
            result += "." + self.visit(node.callee())
        result += "("
        for i in range(len(node.args())):
            result += self.visit(node.args()[i])
            if i < len(node.args()) - 1:
                result += ","
        result += ")"
        return f"{result}"

    def visitFunctionParamList(self, ctx: FunctionParamList):
        return ", ".join(self.visit(param) for param in ctx._params)

    def visitParam(self, ctx: Param):
        mut = "mut " if ctx._is_mutable else ""
        type = ctx._type.accept(self)
        return f"{mut}{ctx._name}: {type}"

    def visitTypedName(self, node):
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
        target = self.visit(node._target)
        value = self.visit(node._value)
        return f"{target} = {value};"

    def visitReturnStmt(self, node):
        if node._value:
            return f"return {self.visit(node._value)};"
        return "return;"

    def visitIfStmt(self, node):
        cond = self.visit(node._condition)
        then = self.visit(node._then_branch)
        result = f"if ({cond}) {then}"
        if node._else_branch:
            result += f" else {self.visit(node._else_branch)}"
        return result

    def visitFieldAccessExpr(self, node: FieldAccessExpr):
        re = ".".join(self.visit(nv) for nv in node.receiver())
        re += "."+self.visit(node.next)
        return f"#[{re}]"

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
        for v in ctx.paths():
            re += self.visit(v)
        return f"{re}" + ";"

    def visitTypePath(self, node: TypePath):
        re = ""
        if node.has_column():
            re += "::"

        for v in node.type():
            re += f"{v}"

        return f"{re}"

    def visitTypedName(self, node: TypedName):
        re = f"{self.visit(node.type())}"
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

    def visitStructDef(self, node: StructDef):
        if node._visibility() is not None:
            re = "pub "
        else:
            re = ""

        re += "struct " + f"{node._name}" + " {"
        for f in node._fields:
            re += f"{self.visit(f)}"
            re += ", "
        re += " }"
        return f"{re}"

    def visitStructField(self, node: StructField):
        if node.visibility() is not None:
            re = "pub "
        else:
            re = ""

        re += f"{node.name()}"
        re += node.type().accept(self)
        return f"{re}"

    def visitStructLiteral(self, node : StructLiteral):
        fields = ", ".join(f"{f._name()}: {self.visit(f._value())}" for f in node._fields())
        return f"{node._name()} {{ {fields} }}"

    def visitUnaryExpr(self, node):
        return f"{node.op()}{self.visit(node.expression())}"

    def visitAttribute(self, node):
        #if node.args:
        #    args_str = ", ".join(self.visit(arg) for arg in node.args)
        #    return f"#[{node.name}({args_str})]"
        return f"#[{node.name()}]"

    def visitFieldAccessExpr(self, node):
        receiver = self.visit(node.receiver())
        return f"{receiver}.{node.next()}"

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