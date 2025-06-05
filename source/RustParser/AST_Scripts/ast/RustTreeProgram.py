from pyggi.tree import TreeProgram
from pyggi.base import AbstractProgram

class RustASTProgram(AbstractProgram):
    def __init__(self, ast):
        super().__init__(path=None)
        self.tree = ast

    def evaluate(self, result=None):
        from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

        checker = TypeChecker()
        checker.visit(self.tree)
        error_count = checker.error_count

        fitness = error_count  
        return {"fitness": fitness}
    
    def get_engine():
        pass
