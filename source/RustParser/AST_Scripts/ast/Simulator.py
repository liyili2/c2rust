import copy
from ast import *
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.Statement import *
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from RustParser.AST_Scripts.ast.ProgramVisitor import ProgramVisitor
from RustParser.AST_Scripts.ast.Expression import *
from RustParser.AST_Scripts.ast.Program import *
from RustParser.AST_Scripts.ast.TopLevel import *

NoneType = type(None)

# I need to add Box maybe?
# I also may need to add arrays

class Simulator(ProgramVisitor):
    # x, y, z, env : ChainMap{ x: n, y : m, z : v} , n m v are nat numbers 100, 100, 100, eg {x : 128}
    # st state map, {x : v1, y : v2 , z : v3}, eg {x : v1}: v1,
    # st {x : v1} --> Coq_nval case: v1 is a ChainMap of Coq_nval
    # v1 --> 128 length array v1: {0 : Coq_nval, 1 : Coq_nval, 2 : Coq_nval, ...., 127 : Coq_nval}, 2^128
    # x --> v1 --> cal(v1) --> integer
    # Coq_nval(b,r) b == |0> | |1>, r == e^(2 pi i * 1 / n), r = 0 Coq_nval(b, 0)
    # x -> v1 ----> run simulator -----> v2 ---> calInt(v2,128) == (x + 2^10) % 2^128
    # Sorry for the late reply Razie. I haven't been able to fully test the simulator yet, but maybe
    def __init__(self, memory: dict, stack: dict):
        # need st --> state we are dealing with
        self.heap = memory
        self.stack = stack
        self.funMap = dict()

    def get_state(self):
        return self.memory

    def get_val_address(self):
        return self.stack

    def get_val(self):
        return self.heap

    def visit(self, ctx):
        return ctx.accept(self)

    def visit_Program(self, ctx: Program):
        for i in ctx.items:
            if not isinstance(i, list):
                i.accept(self)

    def visit_InterfaceDef(self, node: InterfaceDef):
        for fn in node.functions:
            fn.accept(self)

    def visit_LetStmt(self, node: LetStmt):
        newStack = copy.deepcopy(self.stack)

        for i in range(0, len(node.var_defs)):
            arVar = node.var_defs[i].declarationInfo.name
            value = node.values[i].accept(self)
            newStack.update({arVar : value})

        self.stack = newStack
        return None

    def visit_Assignment(self, node: AssignStmt):
        newStack = copy.deepcopy(self.stack)
        target = node.target.name
        value = node.value.accept(self)
        newStack.update({target : value})
        self.stack = newStack
        return None

    def visit_FunctionDef(self, node: FunctionDef):
        self.funMap.update({node.identifier : node})
        if str.__eq__(node.identifier, "main"):
            node.body.accept(self)
        # return_value = node.body.accept(self)
        # if return_value is not None: 
        #     return return_value

    def visit_Block(self, node: Block):
        for stmt in node.stmts:
            if isinstance(stmt, ReturnStmt):
                return stmt.accept(self)
            else:
                stmt.accept(self)

    def visit_FunctionCall(self, node: FunctionCall):
        newNode = self.funMap.get(node.callee.name)
        if newNode is None:
            newNode = self.funMap.get(node.identifier)
        # self.stack.update({"self": node.caller})

        newStack = copy.deepcopy(self.stack)
        for i in range(0, len(newNode.params.params)):
            arVar = newNode.params.params[i].declarationInfo.name
            value = node.args[i].accept(self)
            newStack.update({arVar : value})
        oldStack = self.stack
        self.stack = newStack
        result = newNode.body.accept(self)
        if isinstance(result, IdentifierExpr):
            result = self.stack.get(result.name)
        else:
            result = result.accept(self)

        self.stack = oldStack
        return result

    def visit_IfStmt(self, node: IfStmt):
        if_result = node.condition.accept(self)

        if if_result:
            result = node.then_branch.accept(self)
            return result
        else:
            if node.else_branch is not None:
                result = node.else_branch.accept(self)
                return result

    def visitBreakStmt(self, node: BreakStmt):
        if node is not None: # .vexp()
            return node.accept(self) # .vexp()
        return None # maybe this is better to return?

    def visit_ReturnStmt(self, node: ReturnStmt):
        if node is None:
            return
        else:
            return node.value

    def visit_LoopStmt(self, ctx: LoopStmt):
        # This is the loop keyword. For this type of loop, break statement can return a value
        # A loop statement contains a block statement, and if a break appears in the immediate block statement,
        # this loop will end?
        # The result of a loop comes only from the break statement.
        self.stack_bools.append(True)

        # now, the loop goes into the block
        block_result = ctx.body.accept(self)

        top = self.stack_bools.pop()
        if not top:
            return block_result # this means break statement was called and it is returned back?
        else:
            # call this function again?
            self.visit_LoopStmt(ctx) # is this correct?

        return None

    def visit_ForStmt(self, ctx: ForStmt):
        iterations = ctx.iterable.accept(self)
        self.stack.update({ctx.var: 0})
        while self.stack.get(ctx.var) <= iterations:
            ctx.body.accept(self)
            self.stack.update({ctx.var: self.stack.get(ctx.var) + 1})

    def visit_WhileStmt(self, node: WhileStmt):
        condition = node.condition.accept(self)
        while condition:
            node.body.accept(self)
            condition = node.condition.accept(self)
        return

    def visit_RangeExpression(self, node: RangeExpression):
        last = float(node.last.accept(self))
        first = float(node.initial.accept(self))
        range_len = last - first + 1
        return range_len

    # def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
    #     return

    def visit_FieldAccessExpr(self, node: FieldAccessExpr):
        struct_value = node.receiver.accept(self)            
        for field in struct_value.fields:
            if str.__eq__(node.name.name, field.declarationInfo.name):
                return field.value

    def visit_PatternExpr(self, node: PatternExpr):
        pattern = node.pattern.accept(self)
        if pattern is None:
            return None
        return node.pattern.accept(self)
    
    def visit_BorrowExpr(self, node: BorrowExpr):
        return node.expr.accept(self)

    def visit_SafeWrapper(self, node: SafeWrapper):
        return node.expr.accept(self)

    def visit_StrLiteral(self, ctx: StrLiteral):
        return ctx.value

    def visit_IntLiteral(self, ctx: IntLiteral):
        return ctx.value

    def visit_BoolLiteral(self, ctx: BoolLiteral):
        return ctx.value

    def visit_Struct(self, node: StructDef):
        # Maybe store struct in the stack as a dict or array?
        # self.stack.update(node)
        return node

    def visit_CompoundAssignment(self, node:CompoundAssignment):
        operation = node.op[0]
        assign_Stmt = AssignStmt(target=node.target, value=BinaryExpr(left=node.target, op=operation, right=node.value))
        assign_Stmt.accept(self)

    def visit_BinaryExpr(self, node: BinaryExpr):
        oper = str(node.op)
        # This will be very complicated.
        a = node.left.accept(self)
        
        if isinstance(a, str):
            a = float(a)
        elif a is not None:
            a = a.accept(self)

        if node.right is not None:
            b = node.right.accept(self)
            if isinstance(b, str):
                b = float(b)
            else:
                b = b.accept(self)
                if isinstance(b, str):
                    b = float(b)
        else:
            b = None
        # range is more complicated due to there being an = operator. I can forget about this case for now.
        # Now, I need to write out the cases for each operator.

        if oper == '+':
            return a + b
        elif oper == '-':
            return a - b
        elif oper == '*':
            return a * b
        elif oper == '/':
            return a / b
        elif oper == '%':
            return a % b
        # elif operator == 'Exp':
        #     return pow(a, b)
        elif oper == '&&':
            return a and b
        elif oper == '||':
            return a or b
        elif oper == '<':
            return a < b
        elif oper == '>':
            return a > b
        elif oper == '<=':
            return a <= b
        elif oper == '>=':
            return a >= b
        elif oper == '==':
            return a == b
        elif oper == '!=':
            return a != b
            #return result

        return None

    # def visitBoxWrapperExpr(self, node: BoxWrapperExpr):
    #     return

    # def visitVexp(self, ctx: XMLExpParser.VexpContext):
    #     if ctx.idexp() is not None:
    #         return self.visitIDExp(ctx)
    #     return

    # def visitBoolexp(self, ctx: XMLExpParser.BoolexpContext):
    #     if ctx.TrueLiteral() is not None:
    #         return True
    #     else:
    #         return False

    # def visit(self, ctx: ParserRuleContext):
    #     if ctx.getChildCount() > 0:
    #         return self.visitChildren(ctx)
    #     else:
    #         return self.visitTerminal(ctx)

    # def visit_IdentifierExpr(self, ctx: IdentifierExpr):
    #     return ctx.accept(self)

    def visit_DereferenceExpr(self, node: DereferenceExpr):
        return node.expr.accept(self)

    def visit_IdentifierExpr(self, node: IdentifierExpr):
        identifier_val = self.stack.get(node.name)
        return identifier_val

    # Visit a parse tree produced by XMLExpParser#vexp.
    # def visitVexp(self, ctx: XMLExpParser.VexpContext):
    #     return ctx.numexp().accept(self)