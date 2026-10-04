"""
ast_compare — structural AST equality, ignoring node ids.

Exists so the pipeline and its tests can check "did this actually change?"
without going through RustASTPrinter, which still has open bugs elsewhere.
Once the printer is fixed, dumped-source comparison is the more end-to-end
check to prefer; this is a stand-in until then.
"""
from rust.nodes.ASTNode import CloneableASTNode


def ast_equal(a, b):
    if a is b:
        return True
    if type(a) is not type(b):
        return False
    if isinstance(a, (str, int, float, bool, type(None))):
        return a == b
    if isinstance(a, list):
        return len(a) == len(b) and all(ast_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, CloneableASTNode):
        keys = (set(a.__dict__) | set(b.__dict__)) - {"uid"}
        return all(ast_equal(a.__dict__.get(k), b.__dict__.get(k)) for k in keys)
    return a == b
