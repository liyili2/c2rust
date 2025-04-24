class FunctionDef:
    def __init__(self, identifier, params, return_type, body):
        self.Identifier = identifier
        self.params = params  # list of (name, type)
        self.return_type = return_type
        self.body = body      # list of statements

    def accept(self, visitor):
        method_Identifier = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_Identifier, visitor.generic_visit)(self)

class StructDef:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields  # list of (name, type)

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class Attribute:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)
