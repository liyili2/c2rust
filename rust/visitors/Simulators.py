import copy
from rust.nodes.Statement import *
from rust.visitors.Base import RustASTVisitor
from rust.nodes.Expression import *
from rust.nodes.Program import *
from rust.nodes.TopLevel import *
# from rust.nodes.common import *
from rust.nodes import LibFuncs

NoneType = type(None)

# I need to add Box maybe?
# I also may need to add arrays


class Simulator(RustASTVisitor):
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
        self.stack_bools = []
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

    def visit_Program(self, node: Program):
        # print(ctx.items)
        for i in range(node.length()):
            program_item = node.exp(i)
            if not isinstance(program_item, list):
                if program_item is not None:
                    program_item.accept(self)
                else:
                    print("None type detected in program items")

    def visitInterfaceDef(self, node: InterfaceDef):
        for fn in node.functions:
            fn.accept(self)

    def visitLetStmt(self, node: LetStmt):
        all_var_defs = node.var_defs()
        for i in range(0, len(all_var_defs)):
            arVar = all_var_defs[i].name()
            value = node.values()[i]
            if value is not None:
                value = node.values()[i].accept(self)
            self.stack.update({arVar : value})
        return None

    def find_stack_key(self, target):
        if isinstance(target, IdentifierExpression):
            return target.name()
        if isinstance(target.expression(), IdentifierExpression):
            return target.expression().name()
        if isinstance(target, FieldAccessExpr):
            return self.find_stack_key(target.receiver())
        if isinstance(target, DereferenceExpr):
            return self.find_stack_key(target=target.expression())
        if isinstance(target, BorrowExpression):
            return self.find_stack_key(target=target.expression())
        if isinstance(target, FunctionCallExpression):
            return self.find_stack_key(target.caller())

    def visitAssignment(self, node: AssignStmt):
        newStack = copy.deepcopy(self.stack)
        value = node.value().accept(self)

        if isinstance(node.target(), FieldAccessExpr):
            target = self.find_stack_key(node.target())
            target_original_val = newStack.get(target)
            if isinstance(target_original_val, StructLiteral):
                for field in target_original_val.fields():
                    if str.__eq__(field.name(), node.target().name()):
                        field._value = value
            newStack.update({target : target_original_val})
        else:
            target = self.find_stack_key(node.target())
            newStack.update({target : value})

        self.stack = newStack
        return None
    
    def visitStaticVarDecl(self, node: StaticVarDecl):
        init_val = None
        if node.initial_value is not None:
            init_val = node.initial_value.accept(self)
        self.stack.update({node.declarationInfo.name: init_val})

    def visitFunctionDef(self, node: FunctionDefinition):
        self.funMap.update({node.identifier() : node})
        if str.__eq__(node.identifier(), "main"):
            node.body().accept(self)
        # return_value = node.body.accept(self)
        # if return_value is not None: 
        #     return return_value

    def visitBlock(self, node: Block):
        # try:
        for stmt in node.statements():
            stmt.accept(self)
        # except ReturnSignal as ret:
        #     raise ret
        # return

    def visitFunctionCall(self, node: FunctionCallExpression):
        callee = node.callee()
        args = node.args()
        caller = node.caller()

        if caller is None and isinstance(callee, IdentifierExpression):
            if "print" in callee.name():
                return None

        if isinstance(caller, type(len)):
            if isinstance(callee, IdentifierExpression):
                caller = None
            elif isinstance(callee, FieldAccessExpr):
                caller = callee.receiver

        if isinstance(callee, IdentifierExpression):
            callee = callee.name()
        elif isinstance(callee, FieldAccessExpr):
            callee = callee.receiver().name()

        if callee in self.lib_funcs:
            func = self.libMap.get(callee)
            if func is not None:
                return func(caller=caller, visitor=self, args=args)

        origFunc = self.funMap.get(callee)
        newNode = copy.deepcopy(origFunc)
        if newNode is None:
            newNode = self.funMap.get(callee)
        # self.stack.update({"self": node.caller})
        newStack = copy.deepcopy(self.stack)
        for i in range(0, len(newNode.params)):
            arVar = newNode.params()[i].name() #declarationInfo._name
            value = args[i].accept(self)
            newStack.update({arVar : value})
        oldStack = self.stack
        self.stack = newStack

        result = newNode.body.accept(self)

        if result is not None:
            self.stack = oldStack
            return_val = result
            if isinstance(result, IdentifierExpression): #
                result_val = self.stack.get(result.name())
                self.stack.update({result.name(): result_val})
            return return_val

        self.stack = oldStack
        return None

    def visitIfStmt(self, node: IfStmt):
        if_result = node._condition.accept(self)

        if if_result:
            return node._then_branch.accept(self)
        else:
            if node._else_branch is not None:
                return node._else_branch.accept(self)

    def visitMatchStmt(self, node: MatchStmt):
        match_expr = node.expr.accept(self)
        wildcard_arm = None
        for arm in node.arms:
            patterns = arm.accept(self)
            for pattern in patterns:
                val = pattern.accept(self)

                if val == '_' or val == None:
                    wildcard_arm = arm   # save for later
                elif match_expr == val:
                    return arm._body.accept(self)

        if wildcard_arm:
            return wildcard_arm.body.accept(self)
        return

    def visitMatchArm(self, node: MatchArm):
        match_pattern = node.patterns
        return match_pattern

    def visitMatchPattern(self, node: MatchPattern):
        return node.value.accept(self)

    def visitBreakStmt(self, node: BreakStmt):
        if node is not None: # .vexp()
            return node.accept(self) # .vexp()
        return None # maybe this is better to return?

    def visitReturnStmt(self, node: ReturnStmt):
        val = None
        if hasattr(node, "accept") and callable(node.accept):
            if node.value() is not None:
                val = node.value().accept(self)
        return val
    
    def visitTopLevelVarDef(self, node: TopLevelVarDef):
        value = None
        if node.initial_val is not None:
            value = node.initial_val.accept(self)
        self.stack.update({node.declarationInfo.name : value})

    def visitLoopStmt(self, ctx: LoopStmt):
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
            self.visitLoopStmt(ctx) # is this correct?

        return None

    def visitForStmt(self, ctx: ForStmt):
        iterations = ctx.iterable.accept(self)
        self.stack.update({ctx.var: 0})
        while self.stack.get(ctx.var) < iterations:
            ctx.body.accept(self)
            self.stack.update({ctx.var: self.stack.get(ctx.var) + 1})

    def visitWhileStmt(self, node: WhileStmt):
        condition = node.condition().accept(self)
        while condition:
            node.body().accept(self)
            condition = node.condition().accept(self)
        return

    def visitRangeExpression(self, node: RangeExpression):
        last = float(node.last().accept(self))
        first = float(node.initial().accept(self))
        range_len = last - first + 1
        return range_len

    # def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
    #     return

    def visitExpression(self, node: Expression):
        if isinstance(node, BorrowExpression):
            return node.expression().accept(self)

    def visitFieldAccessExpr(self, node: FieldAccessExpr):
        struct_value = node.receiver().accept(self)

        if isinstance(struct_value, StructDef):
            for field in struct_value._fields:
                if node.next()._name == field.declarationInfo._name:
                    if hasattr(field._value, "accept") and callable(field._value.accept):
                        return field._value.accept(self)
                    return field._value

        return

    def visitint(self, node):
        return node

    def visitByteLiteralExpression(self, node: ByteLiteralExpression):
        return node.value()

    def visitPatternExpr(self, node: PatternExpr):
        pattern = node.pattern().accept(self)
        if pattern is None:
            return None
        return node.pattern().accept(self)

    def visitBorrowExpr(self, node: BorrowExpression):
        return node.expression().accept(self)

    def visitSafeWrapper(self, node: SafeWrapper):
        return node.expression().accept(self)

    def visitStrLiteral(self, ctx: StrLiteral):
        return ctx.value

    def visitIntLiteral(self, ctx: IntLiteral):
        return ctx.value

    def visitBoolLiteral(self, ctx: BooleanLiteral):
        return ctx.value

    def visitArrayLiteral(self, node: ArrayLiteral):
        return node
    
    def visitCharLiteral(self, node: CharLiteral):
        return node.value

    def visitArrayAccess(self, node: ArrayAccess):
        index = node.expression().accept(self)
        target = node.name().accept(self)
        if isinstance(target, ArrayLiteral):
            if hasattr(target.value()[index], "accept") and callable(target.value()[index].accept):
                return (target.value()[index]).accept(self)
            else:
                return target.value()[index]
            
        if hasattr(target[index], "accept") and callable(target[index].accept):
            return (target[index]).accept(self)
        else:
            return target[index]     

    def visitStruct(self, node: StructDef):
        newNode = copy.deepcopy(node)
        for field in newNode.fields():
            if isinstance(field, StructLiteralField):
                if hasattr(field.value, "accept") and callable(field.value.accept):
                    newNode.fields()[field.name()] = field.value.accept(self)

        # self.stack
        return newNode

    def visitCompoundAssignment(self, node:CompoundAssignment):
        operation = node.op[0]
        assign_Stmt = AssignStmt(target=node.target, value=BinaryExpression(left=node.target, op=operation, right=node.value))
        assign_Stmt.accept(self)

    def visitBinaryExpression(self, node: BinaryExpression):
        operator = node.op()
        # This will be very complicated.
        a = node.left().accept(self)

        if node.right() is not None:
            b = node.right().accept(self)
        else:
            b = None
        # range is more complicated due to there being an = operator. I can forget about this case for now.
        # Now, I need to write out the cases for each operator.

        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            return a / b
        elif operator == '%':
            return a % b
        # elif operator == 'Exp':
        #     return pow(a, b)
        elif operator == '&&':
            return a and b
        elif operator == '||':
            return a or b
        elif operator == '<':
            return a < b
        elif operator == '>':
            return a > b
        elif operator == '<=':
            return a <= b
        elif operator == '>=':
            return a >= b
        elif operator == '==':
            return a == b
        elif operator == '!=':
            return a != b
            #return result
        return None
    
    def visitUnaryExpr(self, node: UnaryExpr):
        operator = str(node.op)
        expr = node.expression().accept(self)
        if operator == '-':
            return -expr
        if operator == '+':
            return expr
        if operator == '!':
            return not expr
        else:
            raise Exception(f"Unsupported unary operator: {operator}")

    def visitIdentifierExpression(self, node: IdentifierExpression):
        identifier_val = self.stack.get(node.name())
        return identifier_val

    # TODO: Completely ignore this as these does not affect the answer.
    def visitCastExpr(self, node: CastExpression):
        # print(node.expr)
        cast_result = node.expression().accept(self)
        print(cast_result)
        if isinstance(cast_result, FunctionCallExpression):
            print(cast_result.caller())

        return cast_result

    def visitDereferenceExpr(self, node: DereferenceExpr):
        return node.expression().accept(self)
    
    # def visitTypePathExpression(self, node: TypePathExpression):
    #     return node.last_type

    # library functions

    # def visit_IntoString(self, node: IntoString):
    #
    #     return

    # Visit a parse tree produced by XMLExpParser#vexp.
    # def visitVexp(self, ctx: XMLExpParser.VexpContext):
    #     return ctx.numexp().accept(self)