import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from contextlib import contextmanager
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.MarkedASTNode import MarkedASTNode
from rust.ast.TopLevel import FunctionDef
from rust.modification.Constraint import IsInUnsafeContext

class ASTEditor(RustASTVisitor):

    def __init__(self, constraints=None):
        super().__init__()
        self.edited = []
        self.in_unsafe = False
        self.constraints = constraints if constraints is not None else [IsInUnsafeContext()]
        self.unsafe_marked_nodes = []

    def visit(self, node):
        if node is None:
            return None

        if isinstance(node, (int, str, bool, float)):
            return node

        if isinstance(node, MarkedASTNode):
            if self._should_edit(node):
                if self.in_unsafe:
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

        return super().visit(node)

    def edit(self, root):
        self.edited = []
        self.in_unsafe = False
        self.unsafe_marked_nodes = []
        
        if hasattr(root, "accept"):
            root.accept(self)
        else:
            self.visit(root)
        return root

    @contextmanager
    def _scope_ctx(self, is_unsafe: bool):
        """Safely manages scope entry and exit states."""
        old_unsafe = self.in_unsafe
        if is_unsafe:
            self.in_unsafe = True
        try:
            yield
        finally:
            self.in_unsafe = old_unsafe

    def _should_edit(self, node) -> bool:
        """Evaluates the pipeline of constraints."""
        return all(constraint.matches(node, self) for constraint in self.constraints)

    def apply_edit(self, marked_node):
        return marked_node

    #####################################################
    # Traversal Modifications
    #####################################################

    def visitFunctionDef(self, ctx: FunctionDef):
        is_fn_unsafe = getattr(ctx, "isUnsafe", getattr(ctx, "is_unsafe", False))
        if callable(is_fn_unsafe):
            is_fn_unsafe = is_fn_unsafe()

        with self._scope_ctx(is_unsafe=is_fn_unsafe):
            # Clear the buffer when entering an unsafe function
            if self.in_unsafe:
                self.unsafe_marked_nodes = []

            # Traverse parameters
            if isinstance(ctx.params, list):
                ctx.params = [p.accept(self) if hasattr(p, "accept") else self.visit(p) for p in ctx.params]
            elif ctx.params is not None:
                ctx.params = ctx.params.accept(self) if hasattr(ctx.params, "accept") else self.visit(ctx.params)
                
            # Traverse body (this will populate self.unsafe_marked_nodes via visit())
            if ctx.body is not None:
                ctx.body = ctx.body.accept(self) if hasattr(ctx.body, "accept") else self.visit(ctx.body)
                
            # Traverse return type
            if ctx.return_type:
                ctx.return_type = ctx.return_type.accept(self) if hasattr(ctx.return_type, "accept") else self.visit(ctx.return_type)

            # --- SWAP EXECUTION ---
            # If we found 2 or more marked nodes inside this unsafe function, swap their contents!
            if self.in_unsafe and len(self.unsafe_marked_nodes) > 1:
                self.swap_marked_nodes(self.unsafe_marked_nodes)

        return ctx

    def visitParam(self, ctx):
        """Override base visitor returning True; must return the node itself."""
        return ctx
    
    def swap_marked_nodes(self, marked_nodes):
        """Swaps the internal expressions of the collected MarkedASTNodes via circular rotation."""
        first_content = marked_nodes[0].node
        for i in range(len(marked_nodes) - 1):
            marked_nodes[i].node = marked_nodes[i + 1].node
        marked_nodes[-1].node = first_content