import pytest
import builtins
from rust.visitors.Simulator import Simulator

@pytest.fixture
def simulator():
    mem = dict()
    stack = dict()
    sim = Simulator(memory=mem, stack=stack)
    sim.visit(builtins.ast)
    print("Simulator instance made successdully \n")
    return sim
