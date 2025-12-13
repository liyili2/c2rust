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

def test_match_value(simulator):
    assert simulator.stack.get("MATCH") == 256

def test_split_value(simulator):
    assert simulator.stack.get("SPLIT") == 257

@pytest.mark.parametrize("pattern", [
    b"",
    b"|a",
    b"a|",
    b"*",
    b"+",
    b"?",
    b"(a",
    b"a)",
    b"(a|)",
    b"(|a)",
])
def test_re2post_invalid_patterns(simulator, pattern):
    re2post = simulator.stack["re2post"]
    assert re2post(pattern) is None

def test_re2post_max_length(simulator):
    re2post = simulator.stack["re2post"]
    assert re2post(b"a" * 4000) is not None
    assert re2post(b"a" * 4001) is None
