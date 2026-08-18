from typing import List
from rust.nodes.ASTNode import ASTNode, CloneableASTNode


class Statement(CloneableASTNode):

    def __init__(self, body=None):
        super().__init__()
        self.body = body

    def accept(self, visitor):
        return visitor.visitStatement(self)

    def __body__(self):
        return self.body


class LetStmt(Statement):

    def __init__(self, var_defs, values):
        super().__init__()
        self._var_defs = var_defs if isinstance(var_defs, list) else [var_defs]
        self._values = values if isinstance(values, list) else [values]

    def accept(self, visitor):
        return visitor.visitLetStmt(self)

    def var_defs(self):
        return self._var_defs

    def values(self):
        return self._values


class ForStmt(Statement):
    def __init__(self, var, iterable, body):
        super().__init__()
        self.var = var
        self.iterable = iterable
        self.body = body

    def accept(self, visitor):
        return visitor.visitForStmt(self)

class IfStmt(Statement):

    def __init__(self, condition, then_branch, else_branch=None):
        super().__init__()
        self._condition = condition
        self._then_branch = then_branch
        self._else_branch = else_branch

    def accept(self, visitor):
        return visitor.visitIfStmt(self)

    def condition(self):
        return self._condition

    def then_branch(self):
        return self._then_branch

    def else_branch(self):
        return self._else_branch


class AssignStmt(Statement):

    def __init__(self, target, value):
        super().__init__()
        self._target = target
        self._value = value

    def accept(self, visitor):
        return visitor.visitAssignStmt(self)

    def target(self):
        return self._target

    def value(self):
        return self._value


class ConditionalAssignmentStmt(Statement):
    def __init__(self, cond, body):
        super().__init__()
        self.body = body # assignment stmt
        self.condition = cond
        self.body = body # assignment stmt
        self.condition = cond

    def accept(self, visitor):
        return super().accept(visitor)

class WhileStmt(Statement):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_WhileStmt(self)

class MatchStmt(Statement):
    def __init__(self, expr, arms):
        super().__init__()
        self.expr = expr
        self.arms = arms

    def accept(self, visitor):
        return visitor.visit_MatchStmt(self)

class MatchArm(Statement):
    def __init__(self, patterns, body):
        super().__init__()
        self.patterns = patterns
        self.body = body

    def accept(self, visitor):
        return visitor.visit_MatchArm(self)

class MatchPattern(Statement):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_MatchPattern(self)

class CompoundAssignment(Statement):
    def __init__(self, target, op, value):
        super().__init__()
        self.target = target
        self.op = op
        self.value = value

    def accept(self, visitor):
        return visitor.visitCompoundAssignment(self)


class ReturnStmt(Statement):

    def __init__(self, value=None):
        super().__init__()
        self._value = value

    def accept(self, visitor):
        return visitor.visit_ReturnStmt(self)

    def value(self):
        return self._value


class LoopStmt(Statement):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def accept(self, visitor):
        return visitor.visit_LoopStmt(self)

    def __repr__(self):
        return f"LoopStmt(body={repr(self.body)})"


class BreakStmt(Statement):
    def __init__(self):
        super().__init__()

    def accept(self, visitor):
        return visitor.visit_BreakStmt(self)

class ContinueStmt(Statement):
    def __init__(self):
        super().__init__()
    def accept(self, visitor):
        return visitor.visit_ContinueStmt(self)


class StructDef(Statement):

    def __init__(self, name: str, fields: list):
        super().__init__()
        self.name = name
        self.fields = fields

    def accept(self, visitor):
        return visitor.visitStructDef(self)


class FunctionCall(Statement):
    def __init__(self, callee, args, caller=None):
        super().__init__()
        self.caller = caller
        self.callee = callee
        self.args = args

    def accept(self, visitor):
        return visitor.visitFunctionCall(self)


class Block(Statement):

    def __init__(self, stmts: List[Statement], is_unsafe: bool):
        super().__init__()
        self._stmts = stmts
        self._is_unsafe = is_unsafe

    def accept(self, visitor):
        return visitor.visitBlock(self)

    def statements(self):
        return self._stmts

    def is_unsafe(self):
        return self._is_unsafe


class TypeWrapper(Statement):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_typeWrapper(self)