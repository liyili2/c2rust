import pytest
import builtins
from RustParser.AST_Scripts.ast.Simulator import Simulator

@pytest.fixture
def simulator():
    mem = dict()
    stack = dict()
    sim = Simulator(memory=mem, stack=stack)
    sim.visit(builtins.ast)
    return sim

def test_five_found_value(simulator):
    assert(simulator.stack.get("five_found") == "five")

def test_three_found_value(simulator):
    assert(simulator.stack.get("three_found") == "three")