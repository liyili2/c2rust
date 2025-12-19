import copy
from ast import *
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.Statement import *
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from RustParser.AST_Scripts.ast.ProgramVisitor import ProgramVisitor
from RustParser.AST_Scripts.ast.Expression import *
from RustParser.AST_Scripts.ast.Program import *
from RustParser.AST_Scripts.ast.TopLevel import *
from RustParser.AST_Scripts.ast.common import *
from RustParser.AST_Scripts.ast import LibFuncs

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
    def __init__(self, heap: dict, stack: dict):
        # need st --> state we are dealing with
        self.heap = heap
        self.stack = stack
        self.memory = dict() # store a location and the size of the memory.
        self.funMap = dict()
        self.libMap = dict()
        self.lib_funcs = ["is_empty", "len", "iter", "push", "pop", "null_mut", "into_raw",
                          "into_string", "cast", "is_null", "unwrap","as_ref", "append", "as_bytes", "addr_of_mut!",
                          "fetch_add", "by_ref", "into_boxed_slice", "from", "malloc"]
        self.fill_lib_map()

    def fill_lib_map(self):
        for name in self.lib_funcs:
            parts = name.split('_')
            class_name = "LibFunc" + ''.join(p.capitalize() for p in parts)
            class_name = class_name.replace("!", "")
            cls = getattr(LibFuncs, class_name, None)
            if cls is not None:
                self.libMap[name] = cls()
            else:
                print(f"[warn] Lib function class not found: {class_name}")

    def get_state(self):
        return self.heap

    def get_val_address(self):
        return self.stack

    def get_val(self):
        return self.heap

    def visit(self, ctx):
        return ctx.accept(self)

    def visit_Program(self, ctx: Program):
        # print(ctx.items)
        for i in ctx.items:
            if not isinstance(i, list):
                if i is not None:
                    i.accept(self)
                else:
                    print("None type detected in program items")

    def visit_InterfaceDef(self, node: InterfaceDef):
        for fn in node.functions:
            fn.accept(self)

    def visit_LetStmt(self, node: LetStmt):
        for i in range(0, len(node.var_defs)):
            arVar = node.var_defs[i].declarationInfo.name
            value = node.values[i]
            if value is not None:
                value = node.values[i].accept(self)
            self.stack.update({arVar : value})
        return None

    def find_stack_key(self, target):
        if isinstance(target, IdentifierExpr):
            return target.name
        if isinstance(target.expr, IdentifierExpr):
            return target.expr.name
        if isinstance(target, FieldAccessExpr):
            return self.find_stack_key(target.receiver)
        if isinstance(target, DereferenceExpr):
            return self.find_stack_key(target=target.expr)
        if isinstance(target, BorrowExpr):
            return self.find_stack_key(target=target.expr)
        if isinstance(target, FunctionCall):
            return self.find_stack_key(target.caller)

    def visit_Assignment(self, node: AssignStmt):
        newStack = copy.deepcopy(self.stack)
        value = node.value.accept(self)

        if isinstance(node.target, FieldAccessExpr):
            target = self.find_stack_key(node.target)
            target_original_val = newStack.get(target)
            if isinstance(target_original_val, StructDef):
                for field in target_original_val.fields:
                    if str.__eq__(field.declarationInfo.name, node.target.name.name):
                        field.value = value
            newStack.update({target : target_original_val})
        else:
            target = self.find_stack_key(node.target)
            newStack.update({target : value})

        self.stack = newStack
        return None
    
    def visit_StaticVarDecl(self, node: StaticVarDecl):
        init_val = None
        if node.initial_value is not None:
            init_val = node.initial_value.accept(self)
        self.stack.update({node.declarationInfo.name : init_val})

    def visit_FunctionDef(self, node: FunctionDef):
        self.funMap.update({node.identifier : node})
        if str.__eq__(node.identifier, "main"):
            node.body.accept(self)
        # return_value = node.body.accept(self)
        # if return_value is not None: 
        #     return return_value

    def visit_Block(self, node: Block):
        try:
            for stmt in node.stmts:
                stmt.accept(self)
        except ReturnSignal as ret:
            raise ret

    def visit_FunctionCall(self, node: FunctionCall):
        if node.caller is None and isinstance(node.callee, IdentifierExpr):
            if str.__contains__(node.callee.name, "print"):
                return None

        if isinstance(node.caller, type(len)):
            if isinstance(node.callee, IdentifierExpr):
                node.caller = None
            elif isinstance(node.callee, FieldAccessExpr):
                node.caller = node.callee.receiver
            
        if isinstance(node.callee, IdentifierExpr):
            node.callee = node.callee.name
        elif isinstance(node.callee, FieldAccessExpr):
            node.callee = node.callee.name.name

        if node.callee in self.lib_funcs:
            func = self.libMap.get(node.callee)
            if func is not None:
                # print(func)
                return func(caller=node.caller, visitor=self, args=node.args)

        origFunc = self.funMap.get(node.callee)
        newNode = copy.deepcopy(origFunc)
        if newNode is None:
            newNode = self.funMap.get(node.callee)
        # self.stack.update({"self": node.caller})
        newStack = copy.deepcopy(self.stack)
        for i in range(0, len(newNode.params)):
            arVar = newNode.params.params[i].declarationInfo.name
            value = node.args[i].accept(self)
            newStack.update({arVar : value})
        oldStack = self.stack
        self.stack = newStack
        try:
            newNode.body.accept(self)
        except ReturnSignal as ret:
            self.stack = oldStack
            if isinstance(ret.value, IdentifierExpr):
                ret.value = self.stack.get(ret.value.name)
                self.stack.update({ret.value.name: ret.value})
            return ret.value

        self.stack = oldStack
        print("got none son")
        return None

    def visit_IfStmt(self, node: IfStmt):
        if_result = node.condition.accept(self)

        if if_result:
            return node.then_branch.accept(self)
        else:
            if node.else_branch is not None:
                return node.else_branch.accept(self)

    def visit_MatchStmt(self, node: MatchStmt):
        match_expr = node.expr.accept(self)
        wildcard_arm = None
        for arm in node.arms:
            patterns = arm.accept(self)
            for pattern in patterns:
                val = pattern.accept(self)

                if val == '_' or val == None:
                    wildcard_arm = arm   # save for later
                elif match_expr == val:
                    return arm.body.accept(self)

        if wildcard_arm:
            return wildcard_arm.body.accept(self)
        return

    def visit_MatchArm(self, node: MatchArm):
        match_pattern = node.patterns
        return match_pattern

    def visit_MatchPattern(self, node: MatchPattern):
        return node.value.accept(self)

    def visitBreakStmt(self, node: BreakStmt):
        if node is not None: # .vexp()
            return node.accept(self) # .vexp()
        return None # maybe this is better to return?

    def visit_ReturnStmt(self, node: ReturnStmt):
        val = None
        if hasattr(node, "accept") and callable(node.accept):
            if node.value is not None:
                val = node.value.accept(self)
        raise ReturnSignal(val)
    
    def visit_TopLevelVarDef(self, node: TopLevelVarDef):
        value = None
        if node.initial_val is not None:
            value = node.initial_val.accept(self)
        self.stack.update({ node.declarationInfo.name : value})

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
        while self.stack.get(ctx.var) < iterations:
            ctx.body.accept(self)
            self.stack.update({ctx.var: self.stack.get(ctx.var) + 1})

    def visit_WhileStmt(self, node: WhileStmt):
        condition = node.condition.accept(self)
        while condition:
            node.body.accept(self)
            condition = node.condition.accept(self)
        return

    def visit_MatchArm(self, node: MatchArm):

        match_pattern = node.patterns
        # print(match_pattern)

        return match_pattern

    def visit_MatchPattern(self, node: MatchPattern):

        return node.value.accept(self)

    def visit_RangeExpression(self, node: RangeExpression):
        last = float(node.last.accept(self))
        first = float(node.initial.accept(self))
        range_len = last - first + 1
        return range_len

    # def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
    #     return

    def visit_Expression(self, node: Expression):
        if isinstance(node, BorrowExpr):
            return node.expr.accept(self)

    def visit_FieldAccessExpr(self, node: FieldAccessExpr):
        struct_value = node.receiver.accept(self)

        if isinstance(struct_value, StructDef):
            for field in struct_value.fields:
                if node.name.name == field.declarationInfo.name:
                    if hasattr(field.value, "accept") and callable(field.value.accept):
                        return field.value.accept(self)
                    return field.value

        return

    def visit_int(self, node):
        return node

    def visit_ByteLiteralExpr(self, node:ByteLiteralExpr):
        return node.expr

    def visit_PatternExpr(self, node: PatternExpr):
        pattern = node.pattern.accept(self)
        if pattern is None:
            return None
        return node.pattern.accept(self)

    def visit_BorrowExpr(self, node: BorrowExpr):
        return node.expr.accept(self)

    def visit_SafeWrapper(self, node: SafeWrapper):
        return node.expr.accept(self)
    
    def visit_LiteralExpr(self, node: LiteralExpr):
        return node.expr.accept(self)

    def visit_StrLiteral(self, ctx: StrLiteral):
        return ctx.value

    def visit_IntLiteral(self, ctx: IntLiteral):
        return ctx.value

    def visit_BoolLiteral(self, ctx: BoolLiteral):
        return ctx.value

    def visit_ArrayLiteral(self, node: ArrayLiteral):
        return node
    
    def visit_CharLiteral(self, node: CharLiteral):
        return node.value

    def visit_ArrayAccess(self, node: ArrayAccess):
        index = node.expr.accept(self)
        target = node.name.accept(self)
        if isinstance(target, ArrayLiteral):
            if hasattr(target.elements[index], "accept") and callable(target.elements[index].accept):
                return (target.elements[index]).accept(self)
            else:
                return target.elements[index]
            
        if hasattr(target[index], "accept") and callable(target[index].accept):
            return (target[index]).accept(self)
        else:
            return target[index]     

    def visit_Struct(self, node: StructDef):
        newNode = copy.deepcopy(node)
        for field in newNode.fields:
            if isinstance(field, StructLiteralField):
                if hasattr(field.value, "accept") and callable(field.value.accept):
                    newNode[field.declarationInfo.name] = field.value.accept(self)

        self.stack
        return newNode

    def visit_CompoundAssignment(self, node:CompoundAssignment):
        operation = node.op[0]
        assign_Stmt = AssignStmt(target=node.target, value=BinaryExpr(left=node.target, op=operation, right=node.value))
        assign_Stmt.accept(self)

    def visit_BinaryExpr(self, node: BinaryExpr):
        oper = str(node.op)
        # This will be very complicated.
        a = node.left.accept(self)

        if node.right is not None:
            b = node.right.accept(self)
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
    
    def visit_UnaryExpr(self, node: UnaryExpr):
        oper = str(node.op)
        expr = node.expr.accept(self)
        if oper == '-':
            return -expr
        if oper == '+':
            return expr
        if oper == '!':
            return not expr
        else:
            raise Exception(f"Unsupported unary operator: {oper}")

    def visit_IdentifierExpr(self, node: IdentifierExpr):
        identifier_val = self.stack.get(node.name)
        return identifier_val

    def visit_CastExpr(self, node: CastExpr):
        # print(node.expr)
        cast_result = node.expr.accept(self)
        print(cast_result)
        if isinstance(cast_result, FunctionCall):
            print(cast_result.caller)

        return cast_result

    def visit_DereferenceExpr(self, node: DereferenceExpr):
        return node.expr.accept(self)
    
    def visit_TypePathExpression(self, node: TypePathExpression):
        return node.last_type

    # library functions

    # def visit_IntoString(self, node: IntoString):
    #
    #     return

    # Visit a parse tree produced by XMLExpParser#vexp.
    # def visitVexp(self, ctx: XMLExpParser.VexpContext):
    #     return ctx.numexp().accept(self)