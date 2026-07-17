import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import random
from contextlib import contextmanager
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.MarkedASTNode import MarkedASTNode
from rust.ast.TopLevel import FunctionDef
from rust.modification.Constraint import IsInUnsafeContext

class ASTEditor(RustASTVisitor):

    def __init__(self, constraints=None, rng=None):
        super().__init__()
        self.edited = []
        self.in_unsafe = False
        self.constraints = constraints if constraints is not None else [IsInUnsafeContext()]
        self.unsafe_marked_nodes = []
        self.rng = rng if rng is not None else random.Random()

    def swap_marked_nodes(self, marked_nodes):
        if len(marked_nodes) < 2:
            return
        node_a, node_b = self.rng.sample(marked_nodes, 2)
        node_a.node, node_b.node = node_b.node, node_a.node

    @contextmanager
    def _scope_ctx(self, is_unsafe: bool):
        """Manages per-function scope: tracks unsafe context and gives each
        function its own private buffer of constraint-matched nodes."""
        old_unsafe = self.in_unsafe
        old_marked_nodes = self.unsafe_marked_nodes

        self.in_unsafe = is_unsafe
        self.unsafe_marked_nodes = []   # fresh buffer for every function, not just unsafe ones

        try:
            yield
        finally:
            self.in_unsafe = old_unsafe
            self.unsafe_marked_nodes = old_marked_nodes

    def visit(self, node):
        if node is None:
            return None
        if isinstance(node, (int, str, bool, float)):
            return node
        if isinstance(node, MarkedASTNode):
            return self.visitMarkedASTNode(node)
        return super().visit(node)

    def visitMarkedASTNode(self, node: MarkedASTNode):
        if self._should_edit(node):             # constraint pipeline is now the ONLY gate
            self.unsafe_marked_nodes.append(node)

            if hasattr(node.node, "accept"):
                node.node = node.node.accept(self)
            else:
                node.node = self.visit(node.node)

            replacement = self.apply_edit(node)
            self.edited.append(replacement)
            return replacement
        else:
            inner = node.node
            if hasattr(inner, "accept"):
                node.node = inner.accept(self)
            else:
                node.node = self.visit(inner)
            return node

    def visitFunctionDef(self, ctx: FunctionDef):
        is_fn_unsafe = getattr(ctx, "isUnsafe", getattr(ctx, "is_unsafe", False))
        if callable(is_fn_unsafe):
            is_fn_unsafe = is_fn_unsafe()

        with self._scope_ctx(is_unsafe=is_fn_unsafe):
            if isinstance(ctx.params, list):
                ctx.params = [p.accept(self) if hasattr(p, "accept") else self.visit(p) for p in ctx.params]
            elif ctx.params is not None:
                ctx.params = ctx.params.accept(self) if hasattr(ctx.params, "accept") else self.visit(ctx.params)

            if ctx.body is not None:
                ctx.body = ctx.body.accept(self) if hasattr(ctx.body, "accept") else self.visit(ctx.body)

            if ctx.return_type:
                ctx.return_type = ctx.return_type.accept(self) if hasattr(ctx.return_type, "accept") else self.visit(ctx.return_type)

            # Swap is now purely a function of what the constraints actually matched
            if len(self.unsafe_marked_nodes) > 1:
                self.swap_marked_nodes(self.unsafe_marked_nodes)

        return ctx

    def edit(self, root):
        self.edited = []
        self.in_unsafe = False
        self.unsafe_marked_nodes = []
        
        if hasattr(root, "accept"):
            root.accept(self)
        else:
            self.visit(root)
        return root

    def _should_edit(self, node) -> bool:
        """Evaluates the pipeline of constraints."""
        return all(constraint.matches(node, self) for constraint in self.constraints)

    def apply_edit(self, marked_node):
        return marked_node

    #####################################################
    # Traversal Modifications
    #####################################################

    def visitParam(self, ctx):
        """Override base visitor returning True; must return the node itself."""
        return ctx
    
    # deterministic version
    # def swap_marked_nodes(self, marked_nodes):
    #     """Swaps the internal expressions of the collected MarkedASTNodes via circular rotation."""
    #     first_content = marked_nodes[0].node
    #     for i in range(len(marked_nodes) - 1):
    #         marked_nodes[i].node = marked_nodes[i + 1].node
    #     marked_nodes[-1].node = first_content

    # def swap_marked_nodes(self, marked_nodes):
    #     """Randomly picks two distinct marked nodes and swaps their contents."""
    #     if len(marked_nodes) < 2:
    #         return  # nothing to swap

    #     node_a, node_b = random.sample(marked_nodes, 2)
    #     node_a.node, node_b.node = node_b.node, node_a.node