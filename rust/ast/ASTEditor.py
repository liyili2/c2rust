from rust.ast.MarkedASTNode import MarkedASTNode
from rust.ast.TopLevel import FunctionDef


class ASTEditor:

    def __init__(self):
        self.edited = []

    def edit(self, root):
        self._visit(root, in_unsafe=False)

    #####################################################
    # Traversal
    #####################################################

    def _visit(self, node, in_unsafe):

        if node is None:
            return

        # list of nodes
        if isinstance(node, list):
            self._visit_list(node, in_unsafe)
            return

        # primitive
        if not hasattr(node, "__dict__"):
            return

        # entering an unsafe function
        if isinstance(node, FunctionDef):
            in_unsafe = node.isUnsafe

        # iterate over every field
        for field_name, value in vars(node).items():

            if field_name == "parent":
                continue

            if isinstance(value, list):
                self._edit_list(node, field_name, value, in_unsafe)

            else:
                self._edit_field(node, field_name, value, in_unsafe)

    #####################################################
    # Single field
    #####################################################

    def _edit_field(self, parent, field_name, child, in_unsafe):

        if child is None:
            return

        if isinstance(child, MarkedASTNode):

            if in_unsafe:
                replacement = self.apply_edit(child)

                setattr(parent, field_name, replacement)

                self.edited.append(replacement)

            else:
                # continue traversal inside wrapped node
                self._visit(child.node, in_unsafe)

            return

        self._visit(child, in_unsafe)

    #####################################################
    # List field
    #####################################################

    def _edit_list(self, parent, field_name, children, in_unsafe):

        for i in range(len(children)):

            child = children[i]

            if isinstance(child, MarkedASTNode):

                if in_unsafe:

                    replacement = self.apply_edit(child)

                    children[i] = replacement

                    self.edited.append(replacement)

                else:
                    self._visit(child.node, in_unsafe)

            else:
                self._visit(child, in_unsafe)

    #####################################################
    # Plain list traversal
    #####################################################

    def _visit_list(self, children, in_unsafe):

        for child in children:
            self._visit(child, in_unsafe)

    #####################################################
    # Mutation
    #####################################################

    def apply_edit(self, marked_node):

        """
        Replace this with whatever mutation you want.

        Currently it simply removes the wrapper.
        """

        return marked_node