from ASTNode import ASTNode

class FunctionDef(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params  # list of (name, type)
        self.return_type = return_type
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_def(self)

# class StructDef(ASTNode):
#     def __init__(self, name, fields):
#         self.name = name
#         self.fields = fields  # dict: field_name -> Type

#     def accept(self, visitor):
#         return visitor.visit_struct_def(self)
