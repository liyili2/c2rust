"""
ScopeTrackingGenerator

Single behavior: traverse the AST (via RustASTGenerator's default rebuild) while
maintaining `self._scope` - the variables visible at the node currently being
visited (function params, then each `let` in sequence, restored at block exit).

It changes nothing about the AST. Subclasses add ONE further behavior on top of
the scope they get for free, e.g.:

    RandomCandidateReplacementGenerator   - replaces the selected node
    a scope dumper / type checker / ...   - reads self._scope, records, reports

The three overrides below were moved verbatim out of
RandomCandidateReplacementGenerator, so scope semantics are unchanged.
Place this file next to RandomCandidateReplacementGenerator.py (rust/visitors/).
"""

from rust.visitors.Base import RustASTGenerator
from rust.nodes.TopLevel import FunctionDefinition
from rust.nodes.Statement import Block, LetStmt
from rust.modification.ScopeEnvironment import ScopeEnvironment


class ScopeTrackingGenerator(RustASTGenerator):

    def __init__(self):
        self._scope = ScopeEnvironment()

    def _scope_with_params(self, params) -> ScopeEnvironment:
        scope = ScopeEnvironment()
        if isinstance(params, list):
            for param in params:
                scope = scope.with_binding(param.name(), param.type())
        return scope

    def visitFunctionDefinition(self, node: FunctionDefinition):
        outer_scope = self._scope
        self._scope = self._scope_with_params(node.params())
        try:
            return super().visitFunctionDefinition(node)
        finally:
            self._scope = outer_scope

    def visitBlock(self, node: Block):
        outer_scope = self._scope
        try:
            return super().visitBlock(node)
        finally:
            self._scope = outer_scope

    def visitLetStmt(self, node: LetStmt):
        rebuilt = super().visitLetStmt(node)
        for var_def in node.var_defs():
            self._scope = self._scope.with_binding(var_def.name(), var_def.type())
        return rebuilt
