from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.TopLevel import FunctionDef
from RustParser.AST_Scripts.ast.Block import Block
from RustParser.AST_Scripts.ast.Statement import LetStmt, ForStmt, IfStmt, CallStmt, AssignStmt, WhileStmt
from RustParser.AST_Scripts.ast.Expression import FieldAccessExpr, IdentifierExpr, MethodCallExpr, BinaryExpr
from RustParser.AST_Scripts.ast.Expression import BoolLiteral, IntLiteral, StrLiteral

class MutationUtils:
    def get_all_parents(self, ast_root, target_node, parent=None):
        if parent is None:
            parent = getattr(target_node, 'parent', None)
            if parent is None:
                raise ValueError("Target node has no parent reference")

        if isinstance(parent, Program):
            return [parent]

        return [parent] + self.get_all_parents(ast_root, parent, parent.parent)

    def transform_ast(self, ast_root, target_node, transform_fn):
        parents = self.get_all_parents(ast_root, target_node)
        if not isinstance(ast_root, Program):
            return None

        remaining_tops = []
        parent_len = len(parents)

        for top in ast_root.getChildren():
            if parent_len < 3:
                remaining_tops.append(top)
                continue

            parent_1, parent_2 = parents[-2], parents[-3]
            top_type_matches = isinstance(parent_1, type(top))
            if isinstance(top, list):
                top_children = top
            else:
                top_children = top.getChildren()

            if not top_type_matches:
                remaining_tops.append(top)
                continue

            if isinstance(parent_2, type(top_children)):
                if isinstance(top_children, Block):
                    transform_fn(top, top_children)
                elif isinstance(top_children, FunctionDef) and isinstance(top_children.body, Block):
                    transform_fn(top, top_children.body)

                remaining_tops.append(top)

            elif isinstance(top_children, list):
                matched_children = []
                for item in top_children:
                    if isinstance(parent_2, type(item)) and isinstance(item.body, Block):
                        transform_fn(item, item.body)
                        matched_children.append(item)
                    else:
                        matched_children.append(item)

                top.setFunctions(matched_children)
                remaining_tops.append(top)

        return Program(items=remaining_tops)

    def statements_eq(self, stmt1, stmt2):
        print("statements_eq_", stmt1, stmt2)
        if not isinstance(stmt1, type(stmt2)):
            return False

        if isinstance(stmt1, LetStmt):
            for i in range(len(stmt1.var_defs)):
                if not (str.__eq__(stmt1.var_defs[i].name, stmt2.var_defs[i].name) and isinstance(stmt1.var_defs[i].type, type(stmt2.var_defs[i].type))):
                    print(stmt1.var_defs[i].name, stmt2.var_defs[i].name, stmt1.var_defs[i].type, stmt2.var_defs[i].type)
                    return False
            return True

        if isinstance(stmt1, IfStmt):
            print("ifstmts: ", stmt1.condition , stmt2.condition, stmt1.then_branch , stmt2.then_branch , stmt1.else_branch , stmt2.else_branch)
            return (self.expr_eq(stmt1.condition, stmt2.condition) and
                    self.statements_eq(stmt1.then_branch, stmt2.then_branch) and
                    (stmt1.else_branch is None and stmt2.else_branch is None or
                    stmt1.else_branch is not None and stmt2.else_branch is not None and
                    self.statements_eq(stmt1.else_branch, stmt2.else_branch)))

        if isinstance(stmt1, ForStmt):
            print("forstmt eq case")
            return (
                stmt1.var == stmt2.var and
                self.expr_eq(stmt1.iterable, stmt2.iterable) and
                self.statements_eq(stmt1.body, stmt2.body))

        if isinstance(stmt1, CallStmt):
            if not self.expr_eq(stmt1.callee, stmt2.callee):
                return False
            if len(stmt1.args) != len(stmt2.args):
                return False
            for arg1, arg2 in zip(stmt1.args, stmt2.args):
                if not self.expr_eq(arg1, arg2):
                    return False
            return True

        if isinstance(stmt1, AssignStmt):
            print("assignstmt eq case")
            return (
                self.expr_eq(stmt1.target, stmt2.target) and
                self.expr_eq(stmt1.value, stmt2.value))
        
        if isinstance(stmt1, WhileStmt):
            print("whilestmt eq case")
            return (
                self.expr_eq(stmt1.condition, stmt2.condition) and
                self.statements_eq(stmt1.body, stmt2.body))

        return False

    def expr_eq(self, expr1, expr2):
        if type(expr1) != type(expr2):
            return False
        if isinstance(expr1, IdentifierExpr):
            return expr1.name == expr2.name
        if isinstance(expr1, StrLiteral):
            return expr1.value == expr2.value
        if isinstance(expr1, IntLiteral):
            return expr1.value == expr2.value
        if isinstance(expr1, BoolLiteral):
            return expr1.value == expr2.value
        if isinstance(expr1, BinaryExpr):
            return (self.expr_eq(expr1.left, expr2.left) and
                    self.expr_eq(expr1.right, expr2.right) and
                    expr1.op == expr2.op)
        if isinstance(expr1, MethodCallExpr):
            return (
                self.expr_eq(expr1.receiver, expr2.receiver) and
                expr1.method_name == expr2.method_name and
                len(expr1.args) == len(expr2.args) and
                all(self.expr_eq(a1, a2) for a1, a2 in zip(expr1.args, expr2.args)))
        if isinstance(expr1, FieldAccessExpr):
            return (self.expr_eq(expr1.receiver, expr2.receiver) and self.expr_eq(expr1.name, expr2.name))
        return False 

    def function_def_eq(self, func1, func2):
        # print("function_def_eq", func1.identifier, func2.identifier, (func1.params.param_len), (func2.params.param_len), len(func1.body.getChildren()))
        return (func1.identifier == func2.identifier and (func1.params.param_len) == (func2.params.param_len) and len(func1.body.getChildren()) == len(func1.body.getChildren()))

    def remake_ast_after_removal(self, target_node, other_tops, top, top_children, top_children_stmts):
        for stmt in top_children_stmts:
            if self.statements_eq(stmt, target_node):
                print("equal, applying deletion")
                top_children_stmts.remove(stmt)
                newBlock = Block(top_children_stmts, top_children.isUnsafe)
                top.setBody(newBlock)
                other_tops.append(top)
            else:
                continue

    def blocks_eq(self, block1, block2):
        print("ssss", block1.__class__, block2.__class__)
        if not isinstance(block1, type(block2)):
            return False
        eq = True
        eq = len(block1.getChildren()) == len(block2.getChildren())
        print("eq______", len(block1.getChildren()), len(block2.getChildren()))
        if not eq:
            return eq
        for i in range(len(block1.getChildren())):
            print("eq2______", block1.getChildren()[i], block2.getChildren()[i])
            if not self.statements_eq(block1.getChildren()[i], block2.getChildren()[i]):
                return False

        return True