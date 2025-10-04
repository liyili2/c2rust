import pytest
import builtins
from RustParser.AST_Scripts.ast.Simulator import Simulator

def test_list_len_after_insertion():
    memory = dict()
    stack = dict()
    simulator = Simulator(memory=memory, stack=stack)
    simulator.visit(builtins.ast)
    assert simulator.stack.get("c") == 13