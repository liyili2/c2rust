from abc import ABC, abstractmethod
from rust.nodes.Expression import FunctionCallExpression, TypedName, VarDef, Literal, FieldAccessExpr, RangeExpression, \
    BorrowExpression, TypePath, CastExpression, BinaryExpression, StructLiteral, UnaryExpr, \
    QualifiedExpression, IdentifierExpression, ByteLiteralExpression, ArrayDeclaration, ArrayAccess, \
    DereferenceExpr, ParenExpr, StructLiteralField, PatternExpr, SafeWrapper
from rust.nodes.Func import FunctionParamList, Param
from rust.nodes.ASTNode import MarkedASTNode
from rust.nodes.Program import Program
from rust.nodes.Statement import Block, AssignStmt, ReturnStmt, IfStmt, LetStmt, \
    ForStmt, WhileStmt, MatchStmt, MatchArm, MatchPattern, CompoundAssignment, LoopStmt, BreakStmt, ContinueStmt, FunctionCall
from rust.nodes.Struct import StructField
from rust.nodes.TopLevel import FunctionDefinition, ExternBlock, ExternFunctionDeclaration, UseDecl, StructDef, Attribute
from rust.nodes.Type import BoolType, SignedIntType, StringType, FloatingPointType, ExternalType, UnknownType, PointerType, \
    UnsignedIntType, CharType, SafeNonNullWrapper, ArrayType, PathType, GenericType, ReferenceType, SliceType

class AbstractASTVisitor(ABC):
    def visit(self, node):
        if isinstance(node, MarkedASTNode):
            return self.visitMarkedASTNode(node)
        elif isinstance(node, Program):
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
            return self.visitFloatingPointType(node)
        elif isinstance(node, ExternalType):
            return self.visitExternalType(node)
        elif isinstance(node, UnknownType):
            return self.visitUnknownType(node)
        elif isinstance(node, PointerType):
            return self.visitPointerType(node)
        elif isinstance(node, UnsignedIntType):
            return self.visitUnsignedIntType(node)
        elif isinstance(node, CharType):
            return self.visitCharType(node)
        elif isinstance(node, SafeNonNullWrapper):
            return self.visitSafeNonNullWrapper(node)
        elif isinstance(node, ArrayType):
            return self.visitArrayType(node)
        elif isinstance(node, PathType):
            return self.visitPathType(node)
        elif isinstance(node, GenericType):
            return self.visitGenericType(node)
        elif isinstance(node, ReferenceType):
            return self.visitReferenceType(node)
        elif isinstance(node, SliceType):
            return self.visitSliceType(node)
        elif isinstance(node, QualifiedExpression):
            return self.visitQualifiedExpression(node)
        elif isinstance(node, IdentifierExpression):
            return self.visitIdentifierExpression(node)
        elif isinstance(node, ByteLiteralExpression):
            return self.visitByteLiteralExpression(node)
        elif isinstance(node, ArrayDeclaration):
            return self.visitArrayDeclaration(node)
        elif isinstance(node, ArrayAccess):
            return self.visitArrayAccess(node)
        elif isinstance(node, DereferenceExpr):
            return self.visitDereferenceExpr(node)
        elif isinstance(node, ParenExpr):
            return self.visitParenExpr(node)
        elif isinstance(node, StructLiteralField):
            return self.visitStructLiteralField(node)
        elif isinstance(node, PatternExpr):
            return self.visitPatternExpr(node)
        elif isinstance(node, SafeWrapper):
            return self.visitSafeWrapper(node)
        elif isinstance(node, ForStmt):
            return self.visitForStmt(node)
        elif isinstance(node, WhileStmt):
            return self.visitWhileStmt(node)
        elif isinstance(node, MatchStmt):
            return self.visitMatchStmt(node)
        elif isinstance(node, MatchArm):
            return self.visitMatchArm(node)
        elif isinstance(node, MatchPattern):
            return self.visitMatchPattern(node)
        elif isinstance(node, CompoundAssignment):
            return self.visitCompoundAssignment(node)
        elif isinstance(node, LoopStmt):
            return self.visitLoopStmt(node)
        elif isinstance(node, BreakStmt):
            return self.visitBreakStmt(node)
        elif isinstance(node, ContinueStmt):
            return self.visitContinueStmt(node)
        elif isinstance(node, FunctionCall):
            return self.visitFunctionCall(node)
        else:
            raise Exception(f"Unknown node type: {node}")

    @abstractmethod
    def visitMarkedASTNode(self, node):
        pass

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
    def visitFloatingPointType(self, node):
        pass

    @abstractmethod
    def visitExternalType(self, node):
        pass

    @abstractmethod
    def visitUnknownType(self, node):
        pass

    @abstractmethod
    def visitPointerType(self, node):
        pass

    @abstractmethod
    def visitUnsignedIntType(self, node):
        pass

    @abstractmethod
    def visitCharType(self, node):
        pass

    @abstractmethod
    def visitSafeNonNullWrapper(self, node):
        pass

    @abstractmethod
    def visitArrayType(self, node):
        pass

    @abstractmethod
    def visitPathType(self, node):
        pass

    @abstractmethod
    def visitGenericType(self, node):
        pass

    @abstractmethod
    def visitReferenceType(self, node):
        pass

    @abstractmethod
    def visitSliceType(self, node):
        pass

    @abstractmethod
    def visitQualifiedExpression(self, node):
        pass

    @abstractmethod
    def visitIdentifierExpression(self, node):
        pass

    @abstractmethod
    def visitByteLiteralExpression(self, node):
        pass

    @abstractmethod
    def visitArrayDeclaration(self, node):
        pass

    @abstractmethod
    def visitArrayAccess(self, node):
        pass

    @abstractmethod
    def visitDereferenceExpr(self, node):
        pass

    @abstractmethod
    def visitParenExpr(self, node):
        pass

    @abstractmethod
    def visitStructLiteralField(self, node):
        pass

    @abstractmethod
    def visitPatternExpr(self, node):
        pass

    @abstractmethod
    def visitSafeWrapper(self, node):
        pass

    @abstractmethod
    def visitForStmt(self, node):
        pass

    @abstractmethod
    def visitWhileStmt(self, node):
        pass

    @abstractmethod
    def visitMatchStmt(self, node):
        pass

    @abstractmethod
    def visitMatchArm(self, node):
        pass

    @abstractmethod
    def visitMatchPattern(self, node):
        pass

    @abstractmethod
    def visitCompoundAssignment(self, node):
        pass

    @abstractmethod
    def visitLoopStmt(self, node):
        pass

    @abstractmethod
    def visitBreakStmt(self, node):
        pass

    @abstractmethod
    def visitContinueStmt(self, node):
        pass

    @abstractmethod
    def visitFunctionCall(self, node):
        pass


class RustASTVisitor(AbstractASTVisitor):

    def visitMarkedASTNode(self, node: MarkedASTNode):
        return node.node.accept(self)

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

        if node.return_type():
            dtype = node.return_type().accept(self)
        else:
            dtype = True

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
        callee = node.callee().accept(self) if node.callee() is not None else True
        args = all([arg.accept(self) for arg in node.args()])

        return caller and callee and args

    def visitFunctionParamList(self, node: FunctionParamList):
        return all([p.accept(self) for p in node.params()])

    def visitParam(self, node: Param):
        return node.type().accept(self)

    def visitBlock(self, node: Block):
        return all([statement.accept(self) for statement in node.statements()])

    def visitVarDef(self, node: VarDef):
        return node.type().accept(self) if node.type() is not None else True

    def visitLetStmt(self, node: LetStmt):
        var_defs = all([var_def.accept(self) for var_def in node.var_defs()])
        values = all([value.accept(self) for value in node.values()])

        return var_defs and values

    def visitLiteral(self, node: Literal):
        ntype = node.type().accept(self)

        raw_value = node.value()
        if isinstance(raw_value, list):
            value = all([element.accept(self) for element in raw_value])
        elif hasattr(raw_value, "accept"):
            value = raw_value.accept(self)
        else:
            value = True  # raw scalar (int/bool/str/char) - nothing to traverse

        return ntype and value

    def visitAssignStmt(self, node: AssignStmt):
        target = node.target().accept(self)
        value = node.value().accept(self)

        return target and value

    def visitReturnStmt(self, node: ReturnStmt):
        return node.value().accept(self) if node.value() is not None else True

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
        return all([ntype.accept(self) for ntype in node.type()])

    def visitCastExpression(self, node: CastExpression):
        expression = node.expression().accept(self) if node.expression() is not None else True
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

    def visitFloatingPointType(self, node: FloatingPointType):
        return True

    def visitExternalType(self, node: ExternalType):
        return True

    def visitUnknownType(self, node: UnknownType):
        return True

    def visitPointerType(self, node: PointerType):
        return node.dtype.accept(self)

    def visitUnsignedIntType(self, node: UnsignedIntType):
        return True

    def visitCharType(self, node: CharType):
        return True

    def visitSafeNonNullWrapper(self, node: SafeNonNullWrapper):
        return node.dtype.accept(self)

    def visitArrayType(self, node: ArrayType):
        return node.dtype.accept(self) if node.dtype is not None else True

    def visitPathType(self, node: PathType):
        type_path_ok = node.type_path.accept(self) if hasattr(node.type_path, "accept") else True
        dtype_ok = node.dtype.accept(self) if node.dtype is not None else True
        return type_path_ok and dtype_ok

    def visitGenericType(self, node: GenericType):
        dtypes_ok = all([dtype.accept(self) for dtype in node.generic_dtypes])
        type_path_ok = node.type_path.accept(self) if hasattr(node.type_path, "accept") else True
        return dtypes_ok and type_path_ok

    def visitReferenceType(self, node: ReferenceType):
        return node.dtype.accept(self)

    def visitSliceType(self, node: SliceType):
        return node.dtype.accept(self)

    def visitQualifiedExpression(self, node: QualifiedExpression):
        return node.expression().accept(self)

    def visitIdentifierExpression(self, node: IdentifierExpression):
        return node.type().accept(self) if node.type() is not None else True

    def visitByteLiteralExpression(self, node: ByteLiteralExpression):
        return True  # raw string value, nothing to traverse

    def visitArrayDeclaration(self, node: ArrayDeclaration):
        size_ok = node.size().accept(self) if hasattr(node.size(), "accept") else True
        value_ok = node.value().accept(self) if hasattr(node.value(), "accept") else True
        return size_ok and value_ok

    def visitArrayAccess(self, node: ArrayAccess):
        expression = node.expression().accept(self)
        ntype = node.type().accept(self) if node.type() is not None else True
        return expression and ntype

    def visitDereferenceExpr(self, node: DereferenceExpr):
        return node.expression().accept(self)

    def visitParenExpr(self, node: ParenExpr):
        return node.expression().accept(self)

    def visitStructLiteralField(self, node: StructLiteralField):
        value = node.value().accept(self)
        ntype = node.type().accept(self) if node.type() is not None else True
        return value and ntype

    def visitPatternExpr(self, node: PatternExpr):
        expression = node.expression().accept(self)
        pattern = node.pattern().accept(self) if hasattr(node.pattern(), "accept") else True
        return expression and pattern

    def visitSafeWrapper(self, node: SafeWrapper):
        return node.expression().accept(self)

    def visitForStmt(self, node: ForStmt):
        iterable_ok = node.iterable.accept(self) if hasattr(node.iterable, "accept") else True
        body_ok = node.body.accept(self) if hasattr(node.body, "accept") else True
        return iterable_ok and body_ok

    def visitWhileStmt(self, node: WhileStmt):
        condition_ok = node.condition.accept(self) if hasattr(node.condition, "accept") else True
        body_ok = node.body.accept(self) if hasattr(node.body, "accept") else True
        return condition_ok and body_ok

    def visitMatchStmt(self, node: MatchStmt):
        expr_ok = node.expr.accept(self) if hasattr(node.expr, "accept") else True
        arms_ok = all([arm.accept(self) for arm in node.arms]) if node.arms else True
        return expr_ok and arms_ok

    def visitMatchArm(self, node: MatchArm):
        patterns_ok = all([p.accept(self) for p in node.patterns]) if node.patterns else True
        body_ok = node.body.accept(self) if hasattr(node.body, "accept") else True
        return patterns_ok and body_ok

    def visitMatchPattern(self, node: MatchPattern):
        return node.value.accept(self) if hasattr(node.value, "accept") else True

    def visitCompoundAssignment(self, node: CompoundAssignment):
        target_ok = node.target.accept(self) if hasattr(node.target, "accept") else True
        value_ok = node.value.accept(self) if hasattr(node.value, "accept") else True
        return target_ok and value_ok

    def visitLoopStmt(self, node: LoopStmt):
        return node.body.accept(self) if hasattr(node.body, "accept") else True

    def visitBreakStmt(self, node: BreakStmt):
        return True

    def visitContinueStmt(self, node: ContinueStmt):
        return True

    def visitFunctionCall(self, node: FunctionCall):
        caller_ok = node.caller.accept(self) if hasattr(node.caller, "accept") else True
        callee_ok = node.callee.accept(self) if hasattr(node.callee, "accept") else True
        args_ok = all([arg.accept(self) for arg in node.args]) if node.args else True
        return caller_ok and callee_ok and args_ok


class RustASTGenerator(AbstractASTVisitor):

    def visitMarkedASTNode(self, node: MarkedASTNode):
        return MarkedASTNode(node.node.accept(self)).instance(node.get_id())

    def visitProgram(self, node: Program):
        tmp = []
        i = 0
        while node.exp(i) is not None:
            tmp.append(node.exp(i).accept(self))
            i += 1

        return Program(tmp).instance(node.get_id())

    def visitExternBlock(self, node: ExternBlock):
        program = node.program().accept(self)
        return ExternBlock(node.name(), program).instance(node.get_id())

    def visitExternFunctionDeclaration(self, node: ExternFunctionDeclaration):
        params = [param.accept(self) for param in node.params()]
        return_type = node.return_type().accept(self) if node.return_type() else None

        return ExternFunctionDeclaration(node.name(), params, return_type, node.visibility()).instance(node.get_id())

    def visitFunctionDefinition(self, node: FunctionDefinition):
        params = [param.accept(self) for param in node.params()]
        body = node.body().accept(self)

        return FunctionDefinition(node.identifier(), params, node.return_type(), body, node.is_unsafe()).instance(node.get_id())

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        caller = node.caller().accept(self)
        callee = node.callee().accept(self) if node.callee() is not None else None
        args = [arg.accept(self) for arg in node.args()]

        return FunctionCallExpression(caller, args, callee).instance(node.get_id())

    def visitFunctionParamList(self, node: FunctionParamList):
        params = [p.accept(self) for p in node.params()]
        return FunctionParamList(params).instance(node.get_id())

    def visitParam(self, node: Param):
        ntype = node.type().accept(self)
        return Param(node.name(), ntype, node.is_mutable()).instance(node.get_id())

    def visitBlock(self, node: Block):
        statements = [statement.accept(self) for statement in node.statements()]
        return Block(statements, node.is_unsafe()).instance(node.get_id())

    def visitVarDef(self, node: VarDef):
        ntype = node.type().accept(self) if node.type() is not None else None
        return VarDef(node.name(), node.is_mutable(), node.by_ref(), ntype).instance(node.get_id())

    def visitLetStmt(self, node: LetStmt):
        var_defs = [var_def.accept(self) for var_def in node.var_defs()]
        values = [value.accept(self) for value in node.values()]

        return LetStmt(var_defs, values).instance(node.get_id())

    def visitLiteral(self, node: Literal):
        ntype = node.type().accept(self)

        raw_value = node.value()
        if isinstance(raw_value, list):
            value = [element.accept(self) for element in raw_value]
        elif hasattr(raw_value, "accept"):
            value = raw_value.accept(self)
        else:
            value = raw_value  # raw scalar (int/bool/str/char) - nothing to rebuild

        return Literal(value, ntype).instance(node.get_id())

    def visitAssignStmt(self, node: AssignStmt):
        target = node.target().accept(self)
        value = node.value().accept(self)

        return AssignStmt(target, value).instance(node.get_id())

    def visitReturnStmt(self, node: ReturnStmt):
        value = node.value().accept(self) if node.value() is not None else None
        return ReturnStmt(value).instance(node.get_id())

    def visitIfStmt(self, node: IfStmt):
        condition = node.condition().accept(self)
        then_branch = node.then_branch().accept(self)
        if node.else_branch() is not None:
            else_branch = node.else_branch().accept(self)
        else:
            else_branch = None

        return IfStmt(condition, then_branch, else_branch).instance(node.get_id())

    def visitFieldAccessExpr(self, node: FieldAccessExpr):
        receiver = node.receiver().accept(self)
        nxt = node.next().accept(self)

        return FieldAccessExpr(receiver, nxt).instance(node.get_id())

    def visitRangeExpression(self, node: RangeExpression):
        initial = node.initial().accept(self)
        last = node.last().accept(self)

        return RangeExpression(initial, last).instance(node.get_id())

    def visitBorrowExpression(self, node: BorrowExpression):
        expression = node.expression().accept(self)
        return BorrowExpression(expression, node.is_mutable()).instance(node.get_id())

    def visitUseDecl(self, node: UseDecl):
        paths = [path.accept(self) for path in node.paths()]
        return UseDecl(paths, node.aliases()).instance(node.get_id())

    def visitTypePath(self, node: TypePath):
        return TypePath(node.has_column(), node.type()).instance(node.get_id())

    def visitTypedName(self, node: TypedName):
        ntypes = [ntype.accept(self) for ntype in node.type()]
        return TypedName(node.name(), ntypes).instance(node.get_id())

    def visitCastExpression(self, node: CastExpression):
        expression = node.expression().accept(self) if node.expression() is not None else None
        if node.type() is not None:
            type_expressions = [type_expression.accept(self) for type_expression in node.type()]
        else:
            type_expressions = None

        return CastExpression(expression, type_expressions).instance(node.get_id())

    def visitBinaryExpression(self, node: BinaryExpression):
        left = node.left().accept(self)
        right = node.right().accept(self)

        return BinaryExpression(left, node.op(), right).instance(node.get_id())

    def visitStructDef(self, node: StructDef):
        fields = [field.accept(self) for field in node.fields()]
        return StructDef(node.name(), fields, node.visibility()).instance(node.get_id())

    def visitStructField(self, node: StructField):
        ntype = node.type().accept(self)
        return StructField(node.name(), ntype, node.visibility()).instance(node.get_id())

    def visitStructLiteral(self, node: StructLiteral):
        fields = [field.accept(self) for field in node.fields()]
        return StructLiteral(node.name(), fields).instance(node.get_id())

    def visitUnaryExpr(self, node: UnaryExpr):
        expression = node.expression().accept(self)
        return UnaryExpr(node.op(), expression).instance(node.get_id())

    def visitAttribute(self, node: Attribute):
        return Attribute(node.name(), node.args()).instance(node.get_id())

    def visitBoolType(self, node: BoolType):
        return BoolType().instance(node.get_id())

    def visitSignedIntType(self, node: SignedIntType):
        return SignedIntType(node.ptype()).instance(node.get_id())

    def visitStringType(self, node: StringType):
        return StringType().instance(node.get_id())

    def visitFloatingPointType(self, node: FloatingPointType):
        return FloatingPointType(node.ptype()).instance(node.get_id())

    def visitExternalType(self, node: ExternalType):
        return ExternalType(node.ctype(), node.ptype()).instance(node.get_id())

    def visitUnknownType(self, node: UnknownType):
        return UnknownType(node.ptype()).instance(node.get_id())

    def visitPointerType(self, node: PointerType):
        dtype = node.dtype.accept(self)
        return PointerType(node.mutable, dtype).instance(node.get_id())

    def visitUnsignedIntType(self, node: UnsignedIntType):
        return UnsignedIntType(node.ptype).instance(node.get_id())

    def visitCharType(self, node: CharType):
        return CharType().instance(node.get_id())

    def visitSafeNonNullWrapper(self, node: SafeNonNullWrapper):
        dtype = node.dtype.accept(self)
        return SafeNonNullWrapper(dtype).instance(node.get_id())

    def visitArrayType(self, node: ArrayType):
        dtype = node.dtype.accept(self) if node.dtype is not None else None
        return ArrayType(dtype, node.size).instance(node.get_id())

    def visitPathType(self, node: PathType):
        type_path = node.type_path.accept(self) if hasattr(node.type_path, "accept") else node.type_path
        dtype = node.dtype.accept(self) if node.dtype is not None else None
        return PathType(type_path, dtype).instance(node.get_id())

    def visitGenericType(self, node: GenericType):
        dtypes = [dtype.accept(self) for dtype in node.generic_dtypes]
        type_path = node.type_path.accept(self) if hasattr(node.type_path, "accept") else node.type_path
        return GenericType(dtypes, type_path).instance(node.get_id())

    def visitReferenceType(self, node: ReferenceType):
        dtype = node.dtype.accept(self)
        return ReferenceType(dtype).instance(node.get_id())

    def visitSliceType(self, node: SliceType):
        dtype = node.dtype.accept(self)
        return SliceType(dtype).instance(node.get_id())

    def visitQualifiedExpression(self, node: QualifiedExpression):
        expression = node.expression().accept(self)
        return QualifiedExpression(expression).instance(node.get_id())

    def visitIdentifierExpression(self, node: IdentifierExpression):
        ntype = node.type().accept(self) if node.type() is not None else None
        return IdentifierExpression(node.name(), ntype).instance(node.get_id())

    def visitByteLiteralExpression(self, node: ByteLiteralExpression):
        return ByteLiteralExpression(node.value()).instance(node.get_id())

    def visitArrayDeclaration(self, node: ArrayDeclaration):
        size = node.size().accept(self) if hasattr(node.size(), "accept") else node.size()
        value = node.value().accept(self) if hasattr(node.value(), "accept") else node.value()
        return ArrayDeclaration(node.id(), size, node.force(), value).instance(node.get_id())

    def visitArrayAccess(self, node: ArrayAccess):
        expression = node.expression().accept(self)
        ntype = node.type().accept(self) if node.type() is not None else None
        return ArrayAccess(node.name(), expression, ntype, node.is_mutable(), node.is_unsafe()).instance(node.get_id())

    def visitDereferenceExpr(self, node: DereferenceExpr):
        expression = node.expression().accept(self)
        return DereferenceExpr(expression).instance(node.get_id())

    def visitParenExpr(self, node: ParenExpr):
        expression = node.expression().accept(self)
        return ParenExpr(expression).instance(node.get_id())

    def visitStructLiteralField(self, node: StructLiteralField):
        value = node.value().accept(self)
        ntype = node.type().accept(self) if node.type() is not None else None
        return StructLiteralField(node.name(), value, ntype).instance(node.get_id())

    def visitPatternExpr(self, node: PatternExpr):
        expression = node.expression().accept(self)
        pattern = node.pattern().accept(self) if hasattr(node.pattern(), "accept") else node.pattern()
        return PatternExpr(expression, pattern).instance(node.get_id())

    def visitSafeWrapper(self, node: SafeWrapper):
        expression = node.expression().accept(self)
        return SafeWrapper(expression).instance(node.get_id())

    def visitForStmt(self, node: ForStmt):
        iterable = node.iterable.accept(self) if hasattr(node.iterable, "accept") else node.iterable
        body = node.body.accept(self) if hasattr(node.body, "accept") else node.body
        return ForStmt(node.var, iterable, body).instance(node.get_id())

    def visitWhileStmt(self, node: WhileStmt):
        condition = node.condition.accept(self) if hasattr(node.condition, "accept") else node.condition
        body = node.body.accept(self) if hasattr(node.body, "accept") else node.body
        return WhileStmt(condition, body).instance(node.get_id())

    def visitMatchStmt(self, node: MatchStmt):
        expr = node.expr.accept(self) if hasattr(node.expr, "accept") else node.expr
        arms = [arm.accept(self) for arm in node.arms] if node.arms else node.arms
        return MatchStmt(expr, arms).instance(node.get_id())

    def visitMatchArm(self, node: MatchArm):
        patterns = [p.accept(self) for p in node.patterns] if node.patterns else node.patterns
        body = node.body.accept(self) if hasattr(node.body, "accept") else node.body
        return MatchArm(patterns, body).instance(node.get_id())

    def visitMatchPattern(self, node: MatchPattern):
        value = node.value.accept(self) if hasattr(node.value, "accept") else node.value
        return MatchPattern(value).instance(node.get_id())

    def visitCompoundAssignment(self, node: CompoundAssignment):
        target = node.target.accept(self) if hasattr(node.target, "accept") else node.target
        value = node.value.accept(self) if hasattr(node.value, "accept") else node.value
        return CompoundAssignment(target, node.op, value).instance(node.get_id())

    def visitLoopStmt(self, node: LoopStmt):
        body = node.body.accept(self) if hasattr(node.body, "accept") else node.body
        return LoopStmt(body).instance(node.get_id())

    def visitBreakStmt(self, node: BreakStmt):
        return BreakStmt().instance(node.get_id())

    def visitContinueStmt(self, node: ContinueStmt):
        return ContinueStmt().instance(node.get_id())

    def visitFunctionCall(self, node: FunctionCall):
        caller = node.caller.accept(self) if hasattr(node.caller, "accept") else node.caller
        callee = node.callee.accept(self) if hasattr(node.callee, "accept") else node.callee
        args = [arg.accept(self) for arg in node.args] if node.args else node.args
        return FunctionCall(callee, args, caller).instance(node.get_id())