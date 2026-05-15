import random

class ASTNodeRegistry:
    _nodes: dict[str, "CloneableASTNode"] = {}

    @classmethod
    def register(cls, node: "CloneableASTNode"):
        cls._nodes[node.get_id()] = node
        return node

    @classmethod
    def get(cls, uid: str):
        return cls._nodes.get(uid)

    @classmethod
    def clear(cls):
        cls._nodes.clear()

    @classmethod
    def get_random_marked_node(cls):
        from rust.ast.MarkedASTNode import MarkedASTNode
        # print("registry size: ", len(cls._nodes))
        marked = [n for n in cls._nodes.values() if isinstance(n, MarkedASTNode)]
        return random.choice(marked) if marked else None