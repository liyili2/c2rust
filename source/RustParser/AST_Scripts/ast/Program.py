class Program:
    def __init__(self, items):
        self.items = items  # A list of FunctionDef, StructDef, etc.

    def accept(self, visitor):
        return visitor.visit_Program(self)
