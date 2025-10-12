import pytest
import builtins
from RustParser.AST_Scripts.ast.Simulator import Simulator

def test_list_len_after_insertion():
    mem = dict()
    stack = dict()
    simulator = Simulator(memory=mem, stack=stack)
    simulator.visit(builtins.ast)
    assert(simulator.stack.get("five_found") == "five")
    assert(simulator.stack.get("three_found") == "three")