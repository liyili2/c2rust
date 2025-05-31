from abc import ABC, abstractmethod

class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    def to_dict(self):
        result = {"type": self.__class__.__name__}
        for key, value in vars(self).items():
            if isinstance(value, ASTNode):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, ASTNode) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result