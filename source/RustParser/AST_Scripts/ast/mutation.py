from ast import Expression
import random

from RustParser.AST_Scripts.ast.Expression import IdentifierExpr
from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class ReplaceExpr:
    def create(self, program):
        expr_nodes = collect_exprs(program.tree)
        target = random.choice(expr_nodes)
        replacement = IdentifierExpr(name="42")
        return {"target": target, "replacement": replacement}

    def apply(self, program, modification):
        program.tree.replace_node(modification["target"], modification["replacement"])

def collect_exprs(node):
    result = []
    if isinstance(node, Expression):
        result.append(node)
    for attr in vars(node).values():
        if isinstance(attr, ASTNode):
            result.extend(collect_exprs(attr))
        elif isinstance(attr, list):
            for item in attr:
                if isinstance(item, ASTNode):
                    result.extend(collect_exprs(item))
    return result
