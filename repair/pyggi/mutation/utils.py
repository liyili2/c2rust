class MutationUtils:
    def replace_dereference_with_ref_unwrap_call(stmt):
        new_expr = FunctionCallExpr(caller=FunctionCallExpr(caller=stmt.condition.left.expression,
                                                            callee=IdentifierExpr(name="as_ref")), callee=IdentifierExpr(name="unwrap"))
        return new_expr

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
            elif isinstance(top, StaticVarDecl) or isinstance(top, TypeAliasDecl) or isinstance(top, UseDecl):
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

            elif isinstance(top_children, InterfaceDef):
                matched_children = []
                for item in top_children:
                    if isinstance(parent_2, type(item)) and isinstance(item._body, Block):
                        transform_fn(item, item._body)
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
            for i in range(len(stmt1._var_defs)):
                if not (str.__eq__(stmt1._var_defs[i].declarationInfo._name, stmt2._var_defs[i].declarationInfo._name) and isinstance(stmt1._var_defs[i].declarationInfo._dtype, type(stmt2._var_defs[i].declarationInfo._dtype))):
                    print(stmt1._var_defs[i].declarationInfo._name, stmt2._var_defs[i].declarationInfo._name, stmt1._var_defs[i].declarationInfo._dtype, stmt2._var_defs[i].declarationInfo._dtype)
                    return False
            return True

        if isinstance(stmt1, IfStmt):
            print("ifstmts: ", stmt1._condition, stmt2._condition, stmt1._then_branch, stmt2._then_branch, stmt1._else_branch, stmt2._else_branch)
            return (self.expr_eq(stmt1._condition, stmt2._condition) and
                    self.statements_eq(stmt1._then_branch, stmt2._then_branch) and
                    (stmt1._else_branch is None and stmt2._else_branch is None or
                     stmt1._else_branch is not None and stmt2._else_branch is not None and
                     self.statements_eq(stmt1._else_branch, stmt2._else_branch)))

        if isinstance(stmt1, ForStmt):
            print("forstmt eq case")
            return (
                stmt1.var == stmt2.var and
                self.expr_eq(stmt1.iterable, stmt2.iterable) and
                self.statements_eq(stmt1._body, stmt2._body))

        if isinstance(stmt1, FunctionCall):
            if not self.expr_eq(stmt1.callee, stmt2.callee):
                return False
            if len(stmt1._args) != len(stmt2._args):
                return False
            for arg1, arg2 in zip(stmt1._args, stmt2._args):
                if not self.expr_eq(arg1, arg2):
                    return False
            return True

        if isinstance(stmt1, AssignStmt):
            print("assignstmt eq case")
            return (
                    self.expr_eq(stmt1._target, stmt2._target) and
                    self.expr_eq(stmt1._value, stmt2._value))
        
        if isinstance(stmt1, WhileStmt):
            print("whilestmt eq case")
            return (
                    self.expr_eq(stmt1._condition, stmt2._condition) and
                    self.statements_eq(stmt1._body, stmt2._body))
        
        if isinstance(stmt1, Block):
            for i in range(0, len(stmt1.stmts)):
                if not self.statements_eq(stmt1.stmts[i], stmt2.stmts[i]):
                    return False
            return True

        return False

    def expr_eq(self, expr1, expr2):
        if type(expr1) != type(expr2):
            return False
        if isinstance(expr1, IdentifierExpr):
            return expr1._name == expr2._name
        if isinstance(expr1, StrLiteral):
            return expr1._value == expr2._value
        if isinstance(expr1, IntLiteral):
            return expr1._value == expr2._value
        if isinstance(expr1, BoolLiteral):
            return expr1._value == expr2._value
        if isinstance(expr1, BinaryExpr):
            return (self.expr_eq(expr1.left, expr2.left) and
                    self.expr_eq(expr1.right, expr2.right) and
                    expr1.op == expr2.op)
        if isinstance(expr1, FunctionCall):
            return (
                    self.expr_eq(expr1.caller, expr2.caller) and
                    expr1.callee == expr2.callee and
                    len(expr1._args) == len(expr2._args) and
                    all(self.expr_eq(a1, a2) for a1, a2 in zip(expr1._args, expr2._args)))
        if isinstance(expr1, FieldAccessExpr):
            return (self.expr_eq(expr1.receiver, expr2.receiver) and self.expr_eq(expr1._name, expr2._name))
        if isinstance(expr1, DereferenceExpr):
            return (self.expr_eq(expr1.expression, expr2.expression))
        return False 

    def function_def_eq(self, func1, func2):
        def get_params(f):
            if hasattr(f._params, "params"):
                return f._params._params
            elif isinstance(f._params, list):
                return f._params
            else:
                return []
        params1 = get_params(func1)
        params2 = get_params(func2)
        body1 = func1._body.getChildren() if hasattr(func1._body, "getChildren") else []
        body2 = func2._body.getChildren() if hasattr(func2._body, "getChildren") else []
        return (
            getattr(func1, "identifier", None) == getattr(func2, "identifier", None)
            and len(params1) == len(params2) and len(body1) == len(body2))

    def remake_ast_after_removal(self, target_node, other_tops, top, top_children, top_children_stmts):
        for stmt in top_children_stmts:
            if self.statements_eq(stmt, target_node):
                top_children_stmts.remove(stmt)
                newBlock = Block(top_children_stmts, top_children.is_unsafe)
                top.setBody(newBlock)
                other_tops.append(top)
            else:
                continue

    def blocks_eq(self, block1, block2):
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