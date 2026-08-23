from abc import ABC, abstractmethod
from rust.nodes.ASTNode import MarkedASTNode
from rust.nodes.Expression import FunctionCallExpression, TypedName, VarDef, Literal, FieldAccessExpr, RangeExpression, \
    BorrowExpression, TypePath, CastExpression, BinaryExpression, StructLiteral, UnaryExpr
from rust.nodes.Func import FunctionParamList, Param
from rust.nodes.Program import Program
from rust.nodes.Statement import Block, AssignStmt, ReturnStmt, IfStmt, LetStmt, WhileStmt
from rust.nodes.Struct import StructField
from rust.nodes.TopLevel import FunctionDefinition, ExternBlock, ExternFunctionDeclaration, UseDecl, StructDef, Attribute
from rust.nodes.Type import BoolType, SignedIntType, StringType, FloatingPointType, ExternalType, UnknownType, \
    PointerType


class AbstractASTVisitor(ABC):

    def visit(self, node):
        if isinstance(node, Program):
            return self.visitProgram(node)
        elif isinstance(node, ExternBlock):
            return self.visitExternBlock(node)
        elif isinstance(node, ExternFunctionDeclaration):
            return self.visitExternFunctionDeclaration(node)
        elif isinstance(node, FunctionDefinition):
            return self.visitFunctionDefinition(node)
        elif isinstance(node, FunctionCallExpression):
            return self.visitFunctionCallExpression(node)
        elif isinstance(node, FunctionParamList):
            return self.visitFunctionParamList(node)
        elif isinstance(node, Param):
            return self.visitParam(node)
        elif isinstance(node, TypedName):
            return self.visitTypedName(node)
        elif isinstance(node, Block):
            return self.visitBlock(node)
        elif isinstance(node, LetStmt):
            return self.visitLetStmt(node)
        elif isinstance(node, WhileStmt):
            return self.visitWhileStmt(node)
        elif isinstance(node, VarDef):
            return self.visitVarDef(node)
        elif isinstance(node, Literal):
            return self.visitLiteral(node)
        elif isinstance(node, AssignStmt):
            return self.visitAssignStmt(node)
        elif isinstance(node, ReturnStmt):
            return self.visitReturnStmt(node)
        elif isinstance(node, IfStmt):
            return self.visitIfStmt(node)
        elif isinstance(node, FieldAccessExpr):
            return self.visitFieldAccessExpr(node)
        elif isinstance(node, RangeExpression):
            return self.visitRangeExpression(node)
        elif isinstance(node, BorrowExpression):
            return self.visitBorrowExpression(node)
        elif isinstance(node, UseDecl):
            return self.visitUseDecl(node)
        elif isinstance(node, TypePath):
            return self.visitTypePath(node)
        elif isinstance(node, CastExpression):
            return self.visitCastExpression(node)
        elif isinstance(node, BinaryExpression):
            return self.visitBinaryExpression(node)
        elif isinstance(node, StructDef):
            return self.visitStructDef(node)
        elif isinstance(node, StructField):
            return self.visitStructField(node)
        elif isinstance(node, StructLiteral):
            return self.visitStructLiteral(node)
        elif isinstance(node, UnaryExpr):
            return self.visitUnaryExpr(node)
        elif isinstance(node, Attribute):
            return self.visitAttribute(node)
        elif isinstance(node, BoolType):
            return self.visitBoolType(node)
        elif isinstance(node, SignedIntType):
            return self.visitSignedIntType(node)
        elif isinstance(node, StringType):
            return self.visitStringType(node)
        elif isinstance(node, FloatingPointType):
            return self.visitFloatType(node)
        elif isinstance(node, ExternalType):
            return self.visitExternalType(node)
        elif isinstance(node, UnknownType):
            return self.visitUnknownType(node)
        elif isinstance(node, MarkedASTNode):
            return self.visitMarkedASTNode(node)
        else:
            raise Exception(f"Unknown node type: {node}")

    @abstractmethod
    def visitProgram(self, node):
        pass

    @abstractmethod
    def visitExternBlock(self, node):
        pass

    @abstractmethod
    def visitExternFunctionDeclaration(self, node):
        pass

    @abstractmethod
    def visitFunctionDefinition(self, node):
        pass

    @abstractmethod
    def visitFunctionCallExpression(self, node):
        pass

    @abstractmethod
    def visitFunctionParamList(self, node):
        pass

    @abstractmethod
    def visitParam(self, node):
        pass

    @abstractmethod
    def visitTypedName(self, node):
        pass

    @abstractmethod
    def visitBlock(self, node):
        pass

    @abstractmethod
    def visitLetStmt(self, node):
        pass

    @abstractmethod
    def visitWhileStmt(self, node):
        pass

    @abstractmethod
    def visitVarDef(self, node):
        pass

    @abstractmethod
    def visitLiteral(self, node):
        pass

    @abstractmethod
    def visitAssignStmt(self, node):
        pass

    @abstractmethod
    def visitReturnStmt(self, node):
        pass

    @abstractmethod
    def visitIfStmt(self, node):
        pass

    @abstractmethod
    def visitFieldAccessExpr(self, node):
        pass

    @abstractmethod
    def visitRangeExpression(self, node):
        pass

    @abstractmethod
    def visitBorrowExpression(self, node):
        pass

    @abstractmethod
    def visitUseDecl(self, node):
        pass

    @abstractmethod
    def visitTypePath(self, node):
        pass

    @abstractmethod
    def visitCastExpression(self, node):
        pass

    @abstractmethod
    def visitBinaryExpression(self, node):
        pass

    @abstractmethod
    def visitStructDef(self, node):
        pass

    @abstractmethod
    def visitStructField(self, node):
        pass

    @abstractmethod
    def visitStructLiteral(self, node):
        pass

    @abstractmethod
    def visitUnaryExpr(self, node):
        pass

    @abstractmethod
    def visitAttribute(self, node):
        pass

    @abstractmethod
    def visitBoolType(self, node):
        pass

    @abstractmethod
    def visitSignedIntType(self, node):
        pass

    @abstractmethod
    def visitStringType(self, node):
        pass

    @abstractmethod
    def visitFloatType(self, node):
        pass

    @abstractmethod
    def visitExternalType(self, node):
        pass

    @abstractmethod
    def visitUnknownType(self, node):
        pass

    @abstractmethod
    def visitMarkedASTNode(self, node):
        pass

    @abstractmethod
    def visitPointerType(self, node):
        pass


class RustASTVisitor(AbstractASTVisitor):

    def visitProgram(self, node: Program):
        i = 0
        while node.exp(i) is not None:
            if not node.exp(i).accept(self):
                return False

            i += 1

        return True

    def visitExternBlock(self, node: ExternBlock):
        return node.program().accept(self)

    def visitExternFunctionDeclaration(self, node: ExternFunctionDeclaration):
        params = all([param.accept(self) for param in node.params()])
        dtype = node.return_type().accept(self)

        return params and dtype

    def visitFunctionDefinition(self, node: FunctionDefinition):
        if isinstance(node.params(), list):
            params = all([p.accept(self) for p in node.params()])
        else:
            params = node.params().accept(self)

        body = node.body().accept(self)

        if node.return_type():
            return_type = node.return_type().accept(self)
        else:
            return_type = True

        return params and body and return_type

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        caller = node.caller().accept(self)
        callee = node.callee().accept(self)
        args = all([arg.accept(self) for arg in node.args()])

        return caller and callee and args

    def visitFunctionParamList(self, node: FunctionParamList):
        return all([p.accept(self) for p in node.params()])

    def visitParam(self, node: Param):
        return node.type().accept(self)

    def visitBlock(self, node: Block):
        return all([statement.accept(self) for statement in node.statements()])

    def visitVarDef(self, node: VarDef):
        return node.type().accept(self)

    def visitLetStmt(self, node: LetStmt):
        var_defs = all([var_def.accept(self) for var_def in node.var_defs()])
        values = all([value.accept(self) for value in node.values()])

        return var_defs and values

    def visitWhileStmt(self, node: WhileStmt):
        condition = node.condition().accept(self)
        body = node.body().accept(self)

        return condition and body

    def visitLiteral(self, node: Literal):
        ntype = node.type().accept(self)
        value = node.value().accept(self)

        return ntype and value

    def visitAssignStmt(self, node: AssignStmt):
        target = node.target().accept(self)
        value = node.value().accept(self)

        return target and value

    def visitReturnStmt(self, node: ReturnStmt):
        value = node.value().accept(self)
        return value

    def visitIfStmt(self, node: IfStmt):
        condition = node.condition().accept(self)
        then_branch = node.then_branch().accept(self)
        if node.else_branch() is not None:
            else_branch = node.else_branch().accept(self)
        else:
            else_branch = True

        return condition and then_branch and else_branch

    def visitFieldAccessExpr(self, node: FieldAccessExpr):
        receiver = node.receiver().accept(self)
        next = node.next().accept(self)

        return receiver and next

    def visitRangeExpression(self, node: RangeExpression):
        initial = node.initial().accept(self)
        last = node.last().accept(self)

        return initial and last

    def visitBorrowExpression(self, node: BorrowExpression):
        return node.expression().accept(self)

    def visitUseDecl(self, node: UseDecl):
        return all([path.accept(self) for path in node.paths()])

    def visitTypePath(self, node: TypePath):
        return True

    def visitTypedName(self, node: TypedName):
        return node.type().accept(self)

    def visitCastExpression(self, node: CastExpression):
        expression = node.expression().accept(self)
        btype = True
        if node.type() is not None:
            btype = all([ntype.accept(self) for ntype in node.type()])

        return expression and btype

    def visitBinaryExpression(self, node: BinaryExpression):
        left = node.left().accept(self)
        right = node.right().accept(self)

        return left and right

    def visitStructDef(self, node: StructDef):
        return all([field.accept(self) for field in node.fields()])

    def visitStructField(self, node: StructField):
        return node.type().accept(self)

    def visitStructLiteral(self, node: StructLiteral):
        return all([field.accept(self) for field in node.fields()])

    def visitUnaryExpr(self, node: UnaryExpr):
        return node.expression().accept(self)

    def visitAttribute(self, node: Attribute):
        return True

    def visitBoolType(self, node: BoolType):
        return True

    def visitSignedIntType(self, node: SignedIntType):
        return True

    def visitStringType(self, node: StringType):
        return True

    def visitFloatType(self, node: FloatingPointType):
        return True

    def visitExternalType(self, node: ExternalType):
        return True

    def visitUnknownType(self, node: UnknownType):
        return True

    def visitMarkedASTNode(self, node: MarkedASTNode):
        return node.elem().accept(self)

    def visitPointerType(self, node: PointerType):
        return True


class RustASTGenerator(AbstractASTVisitor):

    def visitProgram(self, node: Program):
        tmp = []
        i = 0
        while node.exp(i) is not None:
            tmp.append(node.exp(i).accept(self))
            i += 1

        return Program(tmp).set_id(node.get_id())

    def visitExternBlock(self, node: ExternBlock):
        program = node.program().accept(self)
        return ExternBlock(node.name(), program).set_id(node.get_id())

    def visitExternFunctionDeclaration(self, node: ExternFunctionDeclaration):
        params = [param.accept(self) for param in node.params()]
        return_type = node.return_type().accept(self)

        return ExternFunctionDeclaration(node.name(), params, return_type, node.visibility()).set_id(node.get_id())

    def visitFunctionDefinition(self, node: FunctionDefinition):
        params = [param.accept(self) for param in node.params()]
        body = node.body().accept(self)

        return FunctionDefinition(node.identifier(), params, node.return_type(), body, node.is_unsafe()).set_id(node.get_id())

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        caller = node.caller().accept(self)
        callee = node.callee().accept(self)
        args = [arg.accept(self) for arg in node.args()]

        return FunctionCallExpression(caller, args, callee).set_id(node.get_id())

    def visitFunctionParamList(self, node: FunctionParamList):
        params = [p.accept(self) for p in node.params()]
        return FunctionParamList(params).set_id(node.get_id())

    def visitParam(self, node: Param):
        ntype = node.type().accept(self)
        return Param(node.name(), ntype, node.is_mutable()).set_id(node.get_id())

    def visitBlock(self, node: Block):
        statements = [statement.accept(self) for statement in node.statements()]
        return Block(statements, node.is_unsafe()).set_id(node.get_id())

    def visitVarDef(self, node: VarDef):
        ntype = node.type().accept(self)
        return VarDef(node.name(), node.is_mutable(), node.by_ref(), ntype).set_id(node.get_id())

    def visitLetStmt(self, node: LetStmt):
        var_defs = [var_def.accept(self) for var_def in node.var_defs()]
        values = [value.accept(self) for value in node.values()]

        return LetStmt(var_defs, values).set_id(node.get_id())

    def visitWhileStmt(self, node: WhileStmt):
        condition = self.visit(node.condition())
        body = self.visit(node.body())

        return WhileStmt(condition, body).set_id(node.get_id())

    def visitLiteral(self, node: Literal):
        ntype = node.type().accept(self)
        value = node.value().accept(self)

        return Literal(value, ntype).set_id(node.get_id())

    def visitAssignStmt(self, node: AssignStmt):
        target = node.target().accept(self)
        value = node.value().accept(self)

        return AssignStmt(target, value).set_id(node.get_id())

    def visitReturnStmt(self, node: ReturnStmt):
        value = node.value().accept(self)
        return ReturnStmt(value).set_id(node.get_id())

    def visitIfStmt(self, node: IfStmt):
        condition = node.condition().accept(self)
        then_branch = node.then_branch().accept(self)
        if node.else_branch() is not None:
            else_branch = node.else_branch().accept(self)
        else:
            else_branch = None

        return IfStmt(condition, then_branch, else_branch).set_id(node.get_id())

    def visitFieldAccessExpr(self, node: FieldAccessExpr):
        receiver = node.receiver().accept(self)
        nxt = node.next().accept(self)

        return FieldAccessExpr(receiver, nxt).set_id(node.get_id())

    def visitRangeExpression(self, node: RangeExpression):
        initial = node.initial().accept(self)
        last = node.last().accept(self)

        return RangeExpression(initial, last).set_id(node.get_id())

    def visitBorrowExpression(self, node: BorrowExpression):
        expression = node.expression().accept(self)
        return BorrowExpression(expression, node.is_mutable()).set_id(node.get_id())

    def visitUseDecl(self, node: UseDecl):
        paths = [path.accept(self) for path in node.paths()]
        return UseDecl(paths, node.aliases()).set_id(node.get_id())

    def visitTypePath(self, node: TypePath):
        return TypePath(node.has_column(), node.type()).set_id(node.get_id())

    def visitTypedName(self, node: TypedName):
        ntypes = [ntype.accept(self) for ntype in node.type()]
        return TypedName(node.name(), ntypes).set_id(node.get_id())

    def visitCastExpression(self, node: CastExpression):
        expression = node.expression().accept(self)
        type_expressions = [type_expression.accept(self) for type_expression in node.type()]

        return CastExpression(expression, type_expressions).set_id(node.get_id())

    def visitBinaryExpression(self, node: BinaryExpression):
        left = node.left().accept(self)
        right = node.right().accept(self)

        return BinaryExpression(left, node.op(), right).set_id(node.get_id())

    def visitStructDef(self, node: StructDef):
        fields = [field.accept(self) for field in node.fields()]
        return StructDef(node.name(), fields, node.visibility()).set_id(node.get_id())

    def visitStructField(self, node: StructField):
        ntype = node.type().accept(self)
        return StructField(node.name(), ntype, node.visibility()).set_id(node.get_id())

    def visitStructLiteral(self, node: StructLiteral):
        fields = [field.accept(self) for field in node.fields()]
        return StructLiteral(node.name(), fields).set_id(node.get_id())

    def visitUnaryExpr(self, node: UnaryExpr):
        expression = node.expression().accept(self)
        return UnaryExpr(node.op(), expression).set_id(node.get_id())

    def visitAttribute(self, node: Attribute):
        return Attribute(node.name(), node.args()).set_id(node.get_id())

    def visitBoolType(self, node: BoolType):
        return BoolType().set_id(node.get_id())

    def visitSignedIntType(self, node: SignedIntType):
        return SignedIntType(node.ptype()).set_id(node.get_id())

    def visitStringType(self, node: StringType):
        return StringType().set_id(node.get_id())

    def visitFloatType(self, node: FloatingPointType):
        return FloatingPointType(node.ptype()).set_id(node.get_id())

    def visitExternalType(self, node: ExternalType):
        return ExternalType(node.ctype(), node.ptype()).set_id(node.get_id())

    def visitUnknownType(self, node: UnknownType):
        return UnknownType(node.ptype()).set_id(node.get_id())

    def visitMarkedASTNode(self, node: MarkedASTNode):
        return MarkedASTNode(node.elem().accept(self)).set_id(node.get_id())

    def visitPointerType(self, node: PointerType):
        return PointerType(node.mutable(), node.type()).set_id(node.get_id())
