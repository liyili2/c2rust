from contextlib import contextmanager
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.MarkedASTNode import MarkedASTNode
from rust.ast.TopLevel import FunctionDef
from rust.modification.Constraint import IsInUnsafeContext

class ASTEditor(RustASTVisitor):

    def __init__(self, constraints=None):
        super().__init__()
        self.edited = []
        self.in_unsafe = False  # Maintained state readable by constraints
        
        # Default to checking unsafe if no custom constraints are passed
        self.constraints = constraints if constraints is not None else [IsInUnsafeContext()]

    def visit(self, node):
        if node is None:
            return None

        # Fix: Intercept raw python primitive types to prevent base match-case crashes
        if isinstance(node, (int, str, bool, float)):
            return node

        # If it's a structural wrapper node, use your editing logic
        if isinstance(node, MarkedASTNode):
            if self._should_edit(node):
                replacement = self.apply_edit(node)
                self.edited.append(replacement)
                return replacement
            else:
                inner = node.node
                return inner.accept(self) if hasattr(inner, "accept") else self.visit(inner)

        # Only pass true ASTNode objects down to your teammate's match statement
        return super().visit(node)

    def edit(self, root):
        self.edited = []
        self.in_unsafe = False
        
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
    # Core Interception Logic
    #####################################################

    def visit(self, node):
        if node is None:
            return None

        if isinstance(node, MarkedASTNode):
            # Enforce constraints structured dynamically
            if self._should_edit(node):
                replacement = self.apply_edit(node)
                self.edited.append(replacement)
                return replacement
            else:
                # Fall through to the underlying node if constraints fail
                inner = node.node
                return inner.accept(self) if hasattr(inner, "accept") else self.visit(inner)

        return super().visit(node)

    #####################################################
    # Traversal Modifications
    #####################################################

    def visitFunctionDef(self, ctx: FunctionDef):
        # Determine if this specific function introduces an unsafe scope
        is_fn_unsafe = getattr(ctx, "isUnsafe", False)

        # Wrap processing in the scope context manager
        with self._scope_ctx(is_unsafe=is_fn_unsafe):
            if isinstance(ctx.params, list):
                ctx.params = [p.accept(self) if hasattr(p, "accept") else self.visit(p) for p in ctx.params]
            elif ctx.params is not None:
                ctx.params = ctx.params.accept(self) if hasattr(ctx.params, "accept") else self.visit(ctx.params)
                
            if ctx.body is not None:
                ctx.body = ctx.body.accept(self) if hasattr(ctx.body, "accept") else self.visit(ctx.body)
                
            if ctx.return_type:
                ctx.return_type = ctx.return_type.accept(self) if hasattr(ctx.return_type, "accept") else self.visit(ctx.return_type)

        return ctx

    def visitParam(self, ctx):
        """Override base visitor returning True; must return the node itself."""
        return ctx
    
    # def visitBinaryExpression(self, node):
    #     # Safely traverse the child branches using accept/visit dispatch
    #     if hasattr(node.left(), "accept"):
    #         node.left().accept(self)
    #     else:
    #         self.visit(node.left())

    #     if hasattr(node.right(), "accept"):
    #         node.right().accept(self)
    #     else:
    #         self.visit(node.right())

    #     # CRITICAL: Always return the node itself to maintain the AST structure
    #     return node
    
    # def visitArrayLiteral(self, node):
    #     # Fix: Capture modifications if child nodes are swapped/edited
    #     if hasattr(node, "elements") and node.elements:
    #         node.elements = [
    #             el.accept(self) if hasattr(el, "accept") else self.visit(el)
    #             for el in node.elements
    #         ]
    #     return node

    # def visitFunctionCallExpression(self, node):
    #     if node.args():
    #         # Adjust if your AST relies on direct property mutation vs helper methods
    #         for arg in node.args():
    #             if hasattr(arg, "accept"):
    #                 arg.accept(self)
    #             else:
    #                 self.visit(arg)
    #     return node

    # def visitIntLiteral(self, node):
    #     return node
