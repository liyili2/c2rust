from abc import ABC, abstractmethod

class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    def to_dict(self):
        def convert(value):
            if isinstance(value, ASTNode):
                # print("********************1")
                return value.to_dict()
            elif isinstance(value, list):
                # print("********************2")
                # print("list is ", len(value), value[0].__class__)
                return [convert(item) for item in value]
            elif isinstance(value, dict):
                # print("********************3")
                return {k: convert(v) for k, v in value.items()}
            else:
                # print("*********************4", value)
                return value

        # print("********************5", self.__class__)
        return {
            "type": self.__class__.__name__,
            **{k: convert(v) for k, v in self.__dict__.items() if not k.startswith('_')}
        }