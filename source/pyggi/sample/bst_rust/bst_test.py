import pytest
import builtins
from RustParser.AST_Scripts.ast.Simulator import Simulator

def test_list_len_after_insertion():
    simulator = Simulator()
    sim_result = simulator.visit(builtins.ast)
    assert len(sim_result.stack) == 3