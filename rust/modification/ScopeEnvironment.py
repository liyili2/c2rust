"""
ScopeEnvironment

A small, explicit abstraction for "what variables are visible right now,
and what type (if known) does each one have". No equivalent utility exists
anywhere in the repository, so this is the one new piece of state needed
to make candidate generation scope-aware instead of program-wide.

Immutable by convention: with_binding() returns a NEW environment rather
than mutating the current one, so entering a function/nested block can
extend it for that subtree only, leaving the caller's copy untouched once
the subtree finishes.

Type comparison is intentionally conservative (see names_matching_type):
a candidate is only ever EXCLUDED on a type mismatch we can actually prove
from both sides being non-None Type nodes. Missing type information never
causes exclusion - per the "don't fake semantic correctness" requirement,
we'd rather offer a slightly-too-permissive candidate list than pretend to
have type information the AST doesn't actually carry.
"""


def _types_comparable(a, b) -> bool:
    if type(a) is not type(b):
        return False
    if hasattr(a, "ptype") and hasattr(b, "ptype"):
        return a.ptype() == b.ptype()
    return True


class ScopeEnvironment:

    def __init__(self, bindings: dict = None):
        self._bindings = dict(bindings) if bindings else {}

    def with_binding(self, name: str, dtype=None) -> "ScopeEnvironment":
        updated = dict(self._bindings)
        updated[name] = dtype
        return ScopeEnvironment(updated)

    def names(self) -> list:
        return list(self._bindings.keys())

    def type_of(self, name: str):
        return self._bindings.get(name)

    def names_excluding(self, excluded_name) -> list:
        return [n for n in self._bindings if n != excluded_name]

    def names_matching_type(self, dtype, excluded_name=None) -> list:
        result = []
        for name, candidate_type in self._bindings.items():
            if name == excluded_name:
                continue
            if dtype is not None and candidate_type is not None and not _types_comparable(dtype, candidate_type):
                continue
            result.append(name)
        return result
