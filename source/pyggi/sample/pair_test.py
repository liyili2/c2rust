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

def test_x_found_value(simulator):
    assert(simulator.stack.get("x_ptr") == 15)

def test_y_found_value(simulator):
    assert(simulator.stack.get("y_ptr") == 40)
