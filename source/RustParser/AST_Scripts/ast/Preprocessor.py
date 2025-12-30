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


class Preprocessor(ProgramVisitor):

    def __init__(self, heap: dict, stack: dict):
        # need st --> state we are dealing with
        #self.heap = heap
        #self.stack = stack
        #self.memory = dict() # store a location and the size of the memory.
        self.funMap = dict()
        #self.libMap = dict()
        #self.lib_funcs = ["is_empty", "len", "iter", "push", "pop", "null_mut", "into_raw",
        #                  "into_string", "cast", "is_null", "unwrap","as_ref", "append", "as_bytes", "addr_of_mut!",
        #                  "fetch_add", "by_ref", "into_boxed_slice", "from", "malloc"]
        #self.fill_lib_map()

    def visitProgram(self, ctx: Program):
            # print(ctx.items)
        for i in ctx.items:
            if not isinstance(i, list):
                if i is not None:
                    i.accept(self)
                else:
                    print("None type detected in program items")

    def visitFunctionDef(self, node: FunctionDef):
        self.funMap.update({node.identifier : ("fun", node.params, node.return_type, node.body)})
        #if str.__eq__(node.identifier, "main"):
        #    node.body.accept(self)
        # return_value = node.body.accept(self)
        # if return_value is not None:
        #     return return_value


    def visitStruct(self, node: StructDef):
        self.funMap.update({node.name : ("struct", node.fields)})

    def visitInterfaceDef(self, node: InterfaceDef):
        for fn in node.functions:
            fn.accept(self)

    def visitStaticVarDecl(self, node: StaticVarDecl):
        self.funMap.update({node.name : ("static", node.var_type, node.isMutable, node.initial_value)})

