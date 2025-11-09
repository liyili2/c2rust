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

# def test_five_found_value(simulator):
#     assert(simulator.stack.get("five_found") == "five")

def test_three_found_value(simulator):
    assert(simulator.stack.get("three_found") == "three")

# def test_seven_found_value(simulator):
#     assert(simulator.stack.get("seven_found") == "seven")

# def test_four_found_value(simulator):
#     assert(simulator.stack.get("four_found") == "four")

# def test_two_found_value(simulator):
#     assert(simulator.stack.get("two_found") == "two")

# def test_six_found_value(simulator):
#     assert(simulator.stack.get("six_found") == "six")

# def test_eight_found_value(simulator):
#     assert(simulator.stack.get("eight_found") == "eight")