from collections import deque
# from types import NoneType

# from Program import *
# from Transformer import *
from ast import *
from Transformer import Transformer
from Statement import *
from TypeChecker import TypeChecker

from collections import ChainMap
from collections import deque

from source.RustParser.AST_Scripts.ast.Expression import *

# from types import NoneType

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
    def __init__(self, memory: dict, stack: dict):
        # need st --> state we are dealing with
        self.heap = memory
        self.stack = stack
        self.funMap = dict()
        # self.heap = {}
        # self.stack_bools = deque()

        # The goal is to enable all the examples (see slack): aggregate.rs, bst.rs, nfa.rs
        # aggregate and bst have some stuff that are missing
        # i may want to model lifetimes as well
        # start with doing the memory for the simulator, and later try and implement the lifetime stuff from rust

        # I should also research rust ast: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_ast/ast/index.html
        # parser -> parse xml into rust, then run the simulator
        # Rust_parser -- P --> AST_P (visitor pattern) --> print out (form a string) the XML form
        # (you can decide how to print out) --> our_parser_will_parse the XML_string to XML_Rust -> use simulator.

        # I should do array, array length?, function, reference type, reference operator, make
        # if left as separate thing, make let statement (maybe)
        # it's fine to have both match and if left.
# xml generated code -> programmer
#memory_life_time: variable -> position
#memory : nat_number -> (offset -> value)
#stack : variable -> value (nat_number, or some other stack value)
#pointer a, a -> address_in_stack, address_in_stack -> memory_field,
#memory_field == value, a is a pointer (associated with the number of data it allocated), memory_field = (value, number_of_fields)
#value = list of_basic_data, number_field n, 0 -> value0 , 1 -> value1 , 2 -> value2, ...., *(a+i) --> memory_field_of_a with the offset_i

# testing the simulator on real rust programs

#--->  XML form of rust programs. how you can test on real rust?

#Rust_parser -- P --> AST_P (visitor pattern) --> print out (form a string) the XML form (you can decide how to print out) --> our_parser_will_parse the XML_string to XML_Rust -> use simulator.

    def get_state(self):
        return self.memory

    def get_val_address(self):
        return self.stack

    def get_val(self):
        return self.heap

    # I need to write the function of these grammar now, not just print them out

    # Let statement should assign something?
    # For now, implement some of the expressions
    def visit_LetStmt(self, ctx: LetStmt):
        x = ctx.var_defs # make idexp return identifier
        y = ctx.values # exp will return the value
        res = ctx.accept()
        self.stack.update({str(x) : y})
        return

    #def visitMatch(self, ctx: XMLProgrammer.QXMatch):
        # I will need to modify things even more or make an entirely new thing just for the match statement (due to
        # the fact that its syntax is very different)
    #    return

    # def visitPrint(self, ctx: XMLProgrammer.QXPrint):
    #     # this prints the stringval, then does something with the exp?
    #     # This would call my printer, I will implement later (will be harder)
    #     print(ctx.str())
    #     return

    def visitFunctionDef(self, node:FunctionDef):
        self.funMap.update({node.identifier : node})
        return None

    def visitCallStmt(self, node: CallStmt):
        newNode = self.funMap.get(node.callee)

        newStack = self.stack.deepCopy()
        for i in len(newNode.params):
            arVar = newNode.params[i]
            value = node.args[i].accept(self)
            newStack.update({arVar : value})
        oldStack = self.stack
        self.stack = newStack
        result = newNode.body.accept(self)
        self.stack = oldStack
        return result


    def visitIfStmt(self, ctx: IfStmt):
        if_result = ctx.accept(self) # .vexp()
        result = None
        if if_result:
            result = ctx.then_branch
        else:
            result = ctx.else_branch


        return result

    def visit_Break(self, ctx: BreakStmt):
        # This will be more complicated due to the different types of loops
        self.stack_bools.pop()
        self.stack_bools.append(False)

        if ctx is not None: # .vexp()
            return ctx.accept(self) # .vexp()
        return None # maybe this is better to return?

    def visit_ReturnStmt(self, ctx: ReturnStmt):
        if ctx.accept(self) is None:
            return
        else:
            return ctx.value

    def visit_LoopStmt(self, ctx: LoopStmt):
        # This is the loop keyword. For this type of loop, break statement can return a value
        # A loop statement contains a block statement, and if a break appears in the immediate block statement,
        # this loop will end?
        # The result of a loop comes only from the break statement.
        self.stack_bools.append(True)

        # now, the loop goes into the block
        block_result = ctx.blockstmt().accept(self)

        top = self.stack_bools.pop()
        if not top:
            return block_result # this means break statement was called and it is returned back?
        else:
            # call this function again?
            self.visit_LoopStmt(ctx) # is this correct?

        return None

    def visit_ForStmt(self, ctx: ForStmt):
        # This is the traditional for loop
        x = ctx.var
        v = self.visit(ctx.accept())
        tmp = self.stack.get(x)
        i = 0
        while i < v:
            self.stack.update({x: v})
            ctx.block().accept(self)
            i = i + 1

        self.stack.update({x: tmp})

    # def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
    #     return

    def visit_StrLiteral(self, ctx: StrLiteral):
        return ctx.value

    def visit_IntLiteral(self, ctx: IntLiteral):
        return ctx.value

    def visit_BoolLiteral(self, ctx: BoolLiteral):
        return ctx.value

    def visit_StructLiteral(self, ctx: StructLiteral):

        # Maybe store struct in the stack as a dict or array?
        struct_fields = ctx.fields
        struct_name = ctx.type_name

        self.stack.update({struct_name: struct_fields})

        return ctx.accept()

    def visit_BinaryExpr(self, ctx: BinaryExpr):
        operator = str(ctx.op)
        # This will be very complicated.
        a = ctx.left
        b = ctx.right
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

    def visit_IdentifierExpr(self, ctx: IdentifierExpr):
        return ctx.accept()

    # Visit a parse tree produced by XMLExpParser#vexp.
    # def visitVexp(self, ctx: XMLExpParser.VexpContext):
    #     return ctx.numexp().accept(self)