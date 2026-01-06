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

    def __init__(self): # , heap: dict, stack: dict
        # need st --> state we are dealing with
        #self.heap = heap
        #self.stack = stack
        #self.memory = dict() # store a location and the size of the memory.
        self.stack = dict()
        self.funMap = dict()
        self.structMap = dict()
        #self.libMap = dict()
        #self.lib_funcs = ["is_empty", "len", "iter", "push", "pop", "null_mut", "into_raw",
        #                  "into_string", "cast", "is_null", "unwrap","as_ref", "append", "as_bytes", "addr_of_mut!",
        #                  "fetch_add", "by_ref", "into_boxed_slice", "from", "malloc"]
        #self.fill_lib_map()

    def visit(self, ctx):
        return ctx.accept(self)

    def visitProgram(self, ctx: Program):
            # print(ctx.items)
        for i in ctx.items:
            if not isinstance(i, list):
                if i is not None:
                    i.accept(self)
                else:
                    print("None type detected in program items")

    def visitStruct(self, node: StructDef):
        newNode = copy.deepcopy(node)
        for field in newNode.fields:
            if isinstance(field, StructLiteralField):
                if hasattr(field.value, "accept") and callable(field.value.accept):
                    newNode[field.declarationInfo.name] = field.value.accept(self)
        return newNode

    def visitFunctionDef(self, node: FunctionDef):
        self.funMap.update({node.identifier : (node.params, node.return_type, node.body)})
        #if str.__eq__(node.identifier, "main"):
        #    node.body.accept(self)
        # return_value = node.body.accept(self)
        # if return_value is not None:
        #     return return_value


    def visitStructDef(self, node: StructDef):
        self.structMap.update({node.name : node.fields})

    def visitInterfaceDef(self, node: InterfaceDef):
        for fn in node.functions:
            fn.accept(self)

    def visitStaticVarDecl(self, node: StaticVarDecl):
        value = None
        if node.initial_value is not None:
            value = node.initial_value
        self.stack.update({ node.name: (value,
                            DeclarationInfo(node.var_type,
                                            None, None, None, node.visibility, node.isMutable, node.isExtern))})

    def visitTopLevelVarDef(self, node: TopLevelVarDef):
        value = None
        if node.initial_val is not None:
            value = node.initial_val
        self.stack.update({ node.name: (value,
                            DeclarationInfo(node.type, node.fields, node.isUnsafe, node.def_kinds, node.visibility))})
