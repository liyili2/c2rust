import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.TopLevel import FunctionDef
from rust.ast.MarkedASTNode import MarkedASTNode


class ASTEditor(RustASTVisitor):
    def __init__(self):
        pass

    def _is_unsafe(self, ctx: FunctionDef) -> bool:
        """Best-effort check across the possible attribute names for unsafe fns."""
        for attr in ("isUnsafe", "is_unsafe", "unsafe", "is_unsafe_fn"):
            if getattr(ctx, attr, False):
                return True
        return False

    def _collect_marked(self, node) -> list:
        """Gather every MarkedASTNode reachable inside `node` without mutating anything."""
        collected = []
        self._collecting = collected
        node.accept(self)
        self._collecting = None
        return collected

    def _shuffle_marked_positions(self, marked_nodes: list) -> None:
        """Randomly permutes the wrapped inner nodes across the collected marked positions."""
        if len(marked_nodes) < 2:
            return
        inner_nodes = [m.node for m in marked_nodes]
        shuffled = inner_nodes[:]
        while shuffled == inner_nodes:
            random.shuffle(shuffled)
        for marked, new_inner in zip(marked_nodes, shuffled):
            marked.node = new_inner

    def visitFunctionDef(self, ctx: FunctionDef):
        if isinstance(ctx.params, list):
            ctx.params = [p.accept(self) for p in ctx.params]
        else:
            ctx.params = ctx.params.accept(self)

        if self._is_unsafe(ctx):
            marked_nodes = self._collect_marked(ctx.body)
            self._shuffle_marked_positions(marked_nodes)
        else:
            ctx.body = ctx.body.accept(self)

        if ctx.return_type:
            ctx.return_type = ctx.return_type.accept(self)
        return ctx

    def visitMarkedASTNode(self, node: MarkedASTNode):
        if getattr(self, "_collecting", None) is not None:
            self._collecting.append(node)
        node.node.accept(self)
        return node