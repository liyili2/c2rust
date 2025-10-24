import pytest
import builtins
from RustParser.AST_Scripts.ast.Simulator import Simulator

def test_list_len_after_insertion():
    mem = dict()
    stack = dict()
    simulator = Simulator(memory=mem, stack=stack)
    simulator.visit(builtins.ast)
    assert(simulator.stack.get("MATCH") == 256)
    assert(simulator.stack.get("SPLIT") == 257)
    assert(len(simulator.stack.get("post")) == 8)
    assert(simulator.stack.get("post").elements[0] == 'a')
    assert(simulator.stack.get("post").elements[1] == 'b')
    assert(simulator.stack.get("post").elements[2] == 'c')
    assert(simulator.stack.get("post").elements[3] == '|')
    assert(simulator.stack.get("post").elements[4] == '*')
    assert(simulator.stack.get("post").elements[5] == '.')
    assert(simulator.stack.get("post").elements[6] == 'd')
    assert(simulator.stack.get("post").elements[7] == '.')
    assert(simulator.stack.get("start").getChild('c') == 97)

