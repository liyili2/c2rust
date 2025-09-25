from abc import ABC, abstractmethod
from RustParser.AST_Scripts.ast.common import DeclarationInfo

class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    def replace_node(self, target, replacement):
        for attr_name in vars(self):
            attr = getattr(self, attr_name)

            if isinstance(attr, ASTNode):
                if attr is target:
                    setattr(self, attr_name, replacement)
                    return True
                elif attr.replace_node(target, replacement):
                    return True
            elif isinstance(attr, list):
                for i, item in enumerate(attr):
                    if isinstance(item, ASTNode):
                        if item is target:
                            attr[i] = replacement
                            return True
                        elif item.replace_node(target, replacement):
                            return True
        return False

    def to_dict(self):
        def convert(value):
            if isinstance(value, ASTNode):
                return value.to_dict()
            elif isinstance(value, list):
                return [convert(item) for item in value]
            elif isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            else:
                return value
        return {
            "type": self.__class__.__name__,
            **{k: convert(v) for k, v in self.__dict__.items() if not k.startswith('_')}
        }
    
class StructField(ASTNode):
    def __init__(self, name, typeExpr, visibility):
        super().__init__()
        self.declarationInfo = DeclarationInfo(name=name, type=typeExpr, visibility=visibility)

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)