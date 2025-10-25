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

def test_post_list_length(simulator):
    post = simulator.stack.get("post")
    assert len(post) == 8

def test_post_list_elements(simulator):
    post = simulator.stack.get("post").elements
    expected = ['a', 'b', 'c', '|', '*', '.', 'd', '.']
    assert post == expected

# def test_start_child_value(simulator):
#     start = simulator.stack.get("start")
#     assert start.getChild('c') == 97
# def test_list_len_after_insertion():
#     mem = dict()
#     stack = dict()
#     simulator = Simulator(memory=mem, stack=stack)
#     simulator.visit(builtins.ast)
#     assert(simulator.stack.get("MATCH") == 256)
#     assert(simulator.stack.get("SPLIT") == 257)
#     assert(len(simulator.stack.get("post")) == 8)
#     assert(simulator.stack.get("post").elements[0] == 'a')
#     assert(simulator.stack.get("post").elements[1] == 'b')
#     assert(simulator.stack.get("post").elements[2] == 'c')
#     assert(simulator.stack.get("post").elements[3] == '|')
#     assert(simulator.stack.get("post").elements[4] == '*')
#     assert(simulator.stack.get("post").elements[5] == '.')
#     assert(simulator.stack.get("post").elements[6] == 'd')
#     assert(simulator.stack.get("post").elements[7] == '.')
#     # assert(simulator.stack.get("start").getChild('c') == 97)

