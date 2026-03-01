import copy, random
from rust.ast import FunctionCall as FunctionCallExpr


class MutationVisitor():
    def __init__(self, original_ast, mutation_const):
        self.mutation_const = mutation_const
        self.original_ast = copy.deepcopy(original_ast)
        self.ast = original_ast

    def visit(self, tree):
        if isinstance(tree, list):
            return [self.visit(child) for child in tree]
        rule_name = tree.__class__.__name__.replace("Context", "")
        method_name = f"visit{rule_name}"
        if str.__eq__("visitGene", method_name):
            method_name = "visitProgram"
        visitor_fn = getattr(self, method_name, None)
        try:
            if visitor_fn is not None:
                return visitor_fn(tree)
            else:
                return self.visitChildren(tree)
        except Exception:
            pass
        return self.ast

    def visitProgram(self, node):
        for i in node.getChildren():
            self.visit(i)
        return self.ast

    def visitStaticVarDecl(self, node:StaticVarDecl):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            node.is_mutable = not node.is_mutable

        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            if not isinstance(node.declarationInfo.dtype, SafeNonNullWrapper):
                node.declarationInfo.dtype = SafeNonNullWrapper(typeExpr=node.declarationInfo.dtype)

    def visitFunctionDef(self, node:FunctionDef):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            node.is_unsafe = False

        self.visit(node.params)
        self.visit(node.body)
        self.visit(node.return_type)

    def visitFunctionParamList(self, node:FunctionParamList):
        for param in node.params:
            self.visit(param)

    def visitParam(self, node:Param):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            if not isinstance(node.declarationInfo.dtype, SafeNonNullWrapper):
                node.declarationInfo.dtype = SafeNonNullWrapper(typeExpr=node.declarationInfo.dtype)

    def visitBlock(self, node: Block):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            node.is_unsafe = False

        for stmt in node.stmts:
            self.visit(stmt)

    def visitLetStmt(self, node: LetStmt):
        for var_def in node.var_defs:
            self.visit(var_def)
        for value in node.values:
            self.visit(value)

    def visitVarDef(self, node:VarDef):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            if not isinstance(node.declarationInfo.dtype, SafeNonNullWrapper):
                node.declarationInfo.dtype = SafeNonNullWrapper(typeExpr=node.declarationInfo.dtype)

        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            node.is_mutable = not node.is_mutable

    def visitStructDef(self, node:StructDef):
        for i in node.getChildren():
            self.visit(i)

    def visitStructField(self, node:StructField):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            if not isinstance(node.declarationInfo.dtype, SafeNonNullWrapper):
                node.declarationInfo.dtype = SafeNonNullWrapper(typeExpr=node.declarationInfo.dtype)

    def visitFieldAccessExpr(self, node:FieldAccessExpr):
        self.visit(node.receiver)
        self.visit(node.name)

    def visitDereferenceExpr(self, node:DereferenceExpr):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const and not isinstance(node, FunctionCallExpr):
            new_call = FunctionCallExpr(caller=FunctionCallExpr
                                        (caller=node.expression, callee="as_ref", args=[]), callee="unwrap", args=[])
            node.__class__ = FunctionCallExpr
            node.__dict__.update(new_call.__dict__)

    def visitBinaryExpr(self, node: BinaryExpr):
        self.visit(node.left)
        self.visit(node.right)

    def visitForStmt(self, node:ForStmt):
        self.visit(node.body)
        self.visit(node.iterable)
        self.visit(node.var)

    def visitIfStmt(self, node:IfStmt):
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch is not None:
            self.visit(node.else_branch)

    def visitAssignStmt(self, node:AssignStmt):
        self.visit(node.target)
        self.visit(node.value)

    def visitReturnStmt(self, node:ReturnStmt):
        self.visit(node.value)
    
    def visitWhileStmt(self, node:WhileStmt):
        self.visit(node.condition)
        self.visit(node.body)
    
    def visitMatchStmt(self, node:MatchStmt):
        self.visit(node.expression)
        for arm in node.arms:
            self.visit(arm)

    def visitMatchArm(self, node:MatchArm):
        for pattern in node.patterns:
            self.visit(pattern)
        self.visit(node.body)

    def visitMatchPattern(self, node:MatchPattern):
        self.visit(node.value)

    def visitCompoundAssignment(self, node:CompoundAssignment):
        self.visit(node.target)
        self.visit(node.value)
    
    def visitLoopStmt(self, node:LoopStmt):
        self.visit(node.body)

    def visitBorrowExpr(self, node: BorrowExpr):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            node.is_mutable = not node.is_mutable
        self.visit(node.expression)

    def visitUnaryExpr(self, node: UnaryExpr):
        self.visit(node.expression)

    def visitRangeExpression(self, node: RangeExpression):
        self.visit(node.initial)
        self.visit(node.last)

    def visitFunctionCall(self, node:FunctionCallExpr):
        self.visit(node.caller)
        self.visit(node.callee)

    def visitCastExpr(self, node: CastExpr):
        self.visit(node.expression)
        self.visit(node.dtype)
        self.visit(node.typePath)

    def visitTypePathExpression(self, node:TypePathExpression):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            if not isinstance(node.last_type, SafeNonNullWrapper):
                node.last_type = SafeNonNullWrapper(typeExpr=node.last_type)

    def visitIdentifierExpr(self, node:IdentifierExpr):
        mutation_probability = random.random()
        if mutation_probability > self.mutation_const:
            node.is_mutable = not node.is_mutable
