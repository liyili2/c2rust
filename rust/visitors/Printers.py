from rust.nodes.ASTNode import MarkedASTNode
from rust.nodes.Expression import BinaryExpression, Expression, FieldAccessExpr, FunctionCallExpression, ArrayLiteral, \
    BorrowExpression, TypePath, RangeExpression, StructLiteral, CastExpression, TypedName, VarDef, Literal, UnaryExpr
from rust.nodes.Func import FunctionParamList, Param
from rust.nodes.Statement import Block, LetStmt, AssignStmt, ReturnStmt, IfStmt
from rust.nodes.Struct import StructField
from rust.nodes.TopLevel import *
from rust.nodes.Type import ExternalType, UnknownType, BoolType, SignedIntType, StringType, FloatingPointType, \
    PointerType
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
        result = node.caller().accept(self)
        if node.callee() is not None:
            result += "." + node.callee().accept(self)
        result += "("
        for i in range(len(node.args())):
            result += node.args()[i].accept(self)
            if i < len(node.args()) - 1:
                result += ","
        result += ")"
        return f"{result}"

    def visitFunctionParamList(self, node: FunctionParamList):
        return ", ".join(param.accept(self) for param in node.params())

    def visitParam(self, node: Param):
        mut = "mut " if node.is_mutable() else ""
        type = node.type().accept(self)
        return f"{mut}{node.name()}: {type}"

    def visitTypedName(self, node: TypedName):
        re = f"{node.type().accept(self)}"
        re += f"{node.name()}"
        return f"{re}"

    def visitBlock(self, node: Block):
        stmts = "\n".join("    " + str(stmt.accept(self)) for stmt in node.statements())
        return "{\n" + stmts + "\n}"

    def visitLetStmt(self, node: LetStmt):
        if len(node.var_defs()) != 0:
            var = node.var_defs()[0].accept(self)
            val = node.values()[0].accept(self)
            return f"let {var} = {val};"

        vars_str = ", ".join(v.accept(self) for v in node.var_defs())
        vals_str = ", ".join(v.accept(self) for v in node.values())
        return f"let ({vars_str}) = ({vals_str});"
    
    def visitVarDef(self, node: VarDef):
        mut = "mut " if getattr(node, "is_mut", False) else ""
        if node.type() is not None:
            return f"{mut}{node.name()}: {node.type().accept(self)}"  # or just node.name if no type
        else:
            return f"{mut}{node.name()}: None"

    def visitLiteral(self, node: Literal):
        if isinstance(node, ArrayLiteral):
            re = "["
            for i in range(len(node.value())):
                re += node.value()[i].accept(self)
                if i < len(node.value()) - 1:
                    re += ","
            re += "]"
        else:
            re = str(node.value())
        return f"{re}"

    def visitAssignStmt(self, node: AssignStmt):
        target = node.target().accept(self)
        value = node.value().accept(self)
        return f"{target} = {value};"

    def visitReturnStmt(self, node: ReturnStmt):
        if node.value():
            return f"return {node.value().accept(self)};"
        return "return;"

    def visitIfStmt(self, node: IfStmt):
        cond = node.condition().accept(self)
        then = node.then_branch().accept(self)
        result = f"if ({cond}) {then}"
        if node.else_branch():
            result += f" else {node.else_branch().accept(self)}"
        return result

    def visitFieldAccessExpr(self, node: FieldAccessExpr):
        re = ".".join(nv.accept(self) for nv in node.receiver())
        re += "." + node.next().accept(self)
        return f"#[{re}]"

    def visitRangeExpression(self, node: RangeExpression):
        re = ""
        re += node.initial().accept(self)
        re += ".."
        re += node.last().accept(self)
        return f"{re}"

    def visitBorrowExpression(self, node: BorrowExpression):
        if node.is_mutable():
            re = "mut "
        else:
            re = ""
        v = node.expression().accept(self)
        return f"{re}" + "&" + f"{v}"

    def visitUseDecl(self, ctx: UseDecl):
        re = ""
        for v in ctx.paths():
            re += v.accept(self)
        return f"{re}" + ";"

    def visitTypePath(self, node: TypePath):
        re = ""
        if node.has_column():
            re += "::"

        for v in node.type():
            re += f"{v}"

        return f"{re}"

    def visitCastExpression(self, ctx: CastExpression):
        re = f"{ctx.expression().accept(self)}"
        for child in ctx.type():
            re = f"{child.accept(self)}"
            re += ","
        return f"{re}"

    def visitBinaryExpression(self, node: BinaryExpression):
        op = node.op()
        left = node.left().accept(self)
        right = node.right().accept(self)
        return f"({left} {op} {right})"

    def visitStructDef(self, node: StructDef):
        if node.visibility() is not None:
            re = "pub "
        else:
            re = ""

        re += "struct " + f"{node.name()}" + " {"
        for f in node.fields():
            re += f"{f.accept(self)}"
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

    def visitStructLiteral(self, node: StructLiteral):
        fields = ", ".join(f"{f.name()}: {f.value().accept(self)}" for f in node.fields())
        return f"{node.name()} {{ {fields} }}"

    def visitUnaryExpr(self, node: UnaryExpr):
        return f"{node.op()}{node.expression().accept(self)}"

    def visitAttribute(self, node: Attribute):
        return f"#[{node.name()}]"

    def visitBoolType(self, node: BoolType):
        return "bool"

    def visitSignedIntType(self, node: SignedIntType):
        return "i32"

    def visitStringType(self, node: StringType):
        return "String"

    def visitFloatType(self, node: FloatingPointType):
        return "f32"

    def visitExternalType(self, node: ExternalType):
        left = node.ctype()
        right = node.ptype()
        return f"{left} + :: + {right}"

    def visitUnknownType(self, node: UnknownType):
        return f"{node.ptype()}"

    def visitMarkedASTNode(self, node: MarkedASTNode):
        return f"<marked>{node.elem().accept(self)}</marked>"

    def visitPointerType(self, node: PointerType):
        return ""