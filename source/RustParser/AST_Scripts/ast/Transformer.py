from antlr4 import TerminalNode
from AST_Scripts.ast.Expression import ArrayLiteral, BinaryExpr, BoolLiteral, BorrowExpr, CastExpr, CharLiteralExpr, DereferenceExpr, FieldAccessExpr, IdentifierExpr, IndexExpr, IntLiteral, MethodCallExpr, RepeatArrayLiteral, StrLiteral
from AST_Scripts.ast.Statement import AssignStmt, CompoundAssignment, ExpressionStmt, ForStmt, IfStmt, LetStmt, MatchArm, MatchPattern, MatchStmt, StaticVarDecl, WhileStmt
from AST_Scripts.antlr.RustVisitor import RustVisitor
from AST_Scripts.ast.TopLevel import ExternBlock, ExternFunctionDecl, ExternStaticVarDecl, ExternTypeDecl, FunctionDef, StructDef, Attribute, TypeAliasDecl, UnionDef
from AST_Scripts.ast.Program import Program
from AST_Scripts.ast.Expression import LiteralExpr
from AST_Scripts.ast.Type import ArrayType, BoolType, IntType, PathType, PointerType, StringType, Type
from AST_Scripts.antlr import RustLexer, RustParser
from AST_Scripts.ast.VarDef import VarDef
from AST_Scripts.antlr import RustParser

class Transformer(RustVisitor):
    def _expr_from_text(self, text):
        text = text.strip()
        if text.isdigit():
            return LiteralExpr(value=int(text))
        elif text.startswith("'") and text.endswith("'"):
            return CharLiteralExpr(text[1:-1])
        try:
            return LiteralExpr(value=float(text))
        except ValueError:
            pass
        return IdentifierExpr(name=text)

    def _basic_type_from_str(self, s: str):
        s = s.strip()
        if s in {"i32", "u32", "f64", "bool", "char", "usize", "isize", "FILE"}:
            return Type()
        if s.startswith("*mut "):
            pointee_type = self._basic_type_from_str(s[5:].strip())
            return PointerType(mutability="mut", pointee_type=pointee_type)
        if s.startswith("*const "):
            pointee_type = self._basic_type_from_str(s[7:].strip())
            return PointerType(mutability="const", pointee_type=pointee_type)        
        if s.startswith("*mut") or s.startswith("*const"):
            if " " in s:
                pointer_type, pointee = s.split(" ", 1)
                if pointer_type == "*mut":
                    return PointerType(mutability="mut", pointee_type=self._basic_type_from_str(pointee.strip()))
                elif pointer_type == "*const":
                    return PointerType(mutability="const", pointee_type=self._basic_type_from_str(pointee.strip()))
            else:
                if s.startswith("*mut"):
                    return PointerType(mutability="mut", pointee_type=self._basic_type_from_str(s[5:].strip()))
                elif s.startswith("*const"):
                    return PointerType(mutability="const", pointee_type=self._basic_type_from_str(s[7:].strip()))
        if "::" in s:
            if ';' in s:
                inner_type_str, _ = s.strip('[]').split(';', 1)
                return inner_type_str.strip().split('::')[-1]
            else:
                return s.strip().split('::')[-1]

        return None

    def _handleChainedMethodCall(self, ctx):
        text = ctx.getText()
        parts = text.split('.')
        receiver = self._expr_from_text(parts[0])
        current = receiver
        for part in parts[1:]:
            # if '(' in part:
            #     method_name = part.split('(')[0]
            #     args_text = part[part.find('(')+1:part.rfind(')')]
            #     print("count is ", ctx.getChildCount(), args)
            #     args = [self._expr_from_text(arg.strip()) for arg in args_text.split(',') if arg.strip()]
            # else:
            method_name = part
            args = []
            print("count is ", ctx.getChildCount())
            for i in range(ctx.getChildCount()):
                    # print("child is ", ctx.getChild(i))
                # if isinstance(ctx.getChild(i), RustParser.RustParser.ArgumentListContext):
                    print(f"Child {i}: {type(ctx.getChild(i))} → {ctx.getChild(i).getText()}")
                    args = [self.visit(child) for child in ctx.getChild(i).expression()]
                    break

            current = MethodCallExpr(receiver=current, method_name=method_name, args=args)
        return current
    
    def visitPostfixExpression(self, ctx):
        expr = self.visit(ctx.primaryExpression())
        i = 1
        while i < ctx.getChildCount():
            token = ctx.getChild(i).getText()

            if token == '(':
                arg_list_ctx = ctx.getChild(i + 1)
                if hasattr(arg_list_ctx, 'expression'):
                    args = [self.visit(e) for e in arg_list_ctx.expression()]
                else:
                    args = []
                expr = MethodCallExpr(receiver=expr, method_name=None, args=args)
                i += 3

            elif token == '.':
                next_token = ctx.getChild(i + 1)
                method_or_field = next_token.getText()
                if (i + 2 < ctx.getChildCount() and ctx.getChild(i + 2).getText() in ['(', '()']):
                    if ctx.getChild(i + 2).getText() == '()':
                        args = []
                        i += 3
                    else:
                        arg_list_ctx = ctx.getChild(i + 3)
                        if hasattr(arg_list_ctx, 'expression'):
                            args = [self.visit(e) for e in arg_list_ctx.expression()]
                        else:
                            args = []
                        i += 5
                    expr = MethodCallExpr(receiver=expr, method_name=method_or_field, args=args)
                else:
                    expr = FieldAccessExpr(receiver=expr, field_name=method_or_field)
                    i += 2
            elif token == '[':
                index_expr = self.visit(ctx.getChild(i + 1))
                expr = IndexExpr(target=expr, index=index_expr)
                i += 3
            else:
                i += 1
        return expr

    def visitFieldAccessExpr(self, expr):
        receiver_val = self.visit(expr.receiver)        
        field_name = expr.field_name
        if isinstance(receiver_val, dict):
            if field_name in receiver_val:
                return receiver_val[field_name]
            else:
                raise Exception(f"Field '{field_name}' not found in {receiver_val}")
        else:
            raise Exception(f"Cannot access field '{field_name}' on non-object type: {type(receiver_val)}")

    def visitIndexExpr(self, expr):
        target_val = self.visit(expr.target)
        index_val = self.visit(expr.index)
        try:
            return target_val[index_val]
        except (IndexError, TypeError, KeyError) as e:
            raise Exception(f"Indexing error: {e}")

    def visit_Program(self, ctx):
        items = []
        for item in ctx.topLevelItem():
            result = self.visit(item)
            items.append(result)
        return Program(items)

    def get_literal_type(self, value):
        if isinstance(value, IntLiteral):
            return IntType()
        elif isinstance(value, StrLiteral):
            return StringType()
        elif isinstance(value, BoolLiteral):
            return BoolType()
        elif isinstance(value, ArrayLiteral):
            return ArrayType()
        else:
            raise Exception(f"❌ Unknown literal type for value: {repr(value)}")

    def visitTopLevelItem(self, ctx):
        for child in ctx.getChildren():
            result = self.visit(child)
            if result is not None:
                return result
        print("⚠️ Unrecognized topLevelItem:", ctx.getText())
        return None
    
    def visitTypeAlias(self, ctx):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        name = ctx.Identifier().getText()
        target_type = self.visit(ctx.type_())
        return TypeAliasDecl(name=name, target_type=target_type, visibility=visibility)

    def visitUnionDef(self, ctx):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        name = ctx.Identifier().getText()

        fields = []
        for field_ctx in ctx.unionField():
            if field_ctx.getText() in ['{', '}', ',']:
                continue
            field_name = field_ctx.Identifier().getText()
            field_visibility = field_ctx.visibility().getText() if field_ctx.visibility() else None
            field_type = self.visit(field_ctx.type_())
            fields.append((field_name, field_type, field_visibility))

        return UnionDef(name=name, fields=fields, visibility=visibility)

    def visitFunctionDef(self, ctx):
        name = ctx.Identifier().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        return_type = self.visit(ctx.type_()) if ctx.type_() else None
        body = self.visit(ctx.block())
        return FunctionDef(identifier=name, params=params, return_type=return_type, body=body)

    def visitStructDef(self, ctx):
        name = ctx.Identifier().getText()
        fields = [self.visit(f) for f in ctx.structField()]
        return StructDef(name=name, fields=fields)

    def visitStructField(self, ctx):
        field_name = ctx.Identifier().getText()
        field_type = self.visit(ctx.type_())
        return (field_name, field_type)

    def visitAttributes(self, ctx):
        return [self.visit(inner) for inner in ctx.innerAttribute()]

    def visitInnerAttribute(self, ctx):
        return self.visit(ctx.attribute())

    def visitAttribute(self, ctx):
        name = ctx.Identifier().getText()
        if ctx.attrValue():  # Case: name = value
            value = self.visit(ctx.attrValue())
            return Attribute(name=name, value=value)
        elif ctx.attrArgs():  # Case: name(args)
            args = self.visit(ctx.attrArgs())
            return Attribute(name=name, args=args)
        else:  # Case: plain name
            return Attribute(name=name)

    def visitAttrArgs(self, ctx):
        return [self.visit(arg) for arg in ctx.attrArg()]

    def visitAttrArg(self, ctx):
        name = ctx.Identifier().getText()
        if ctx.attrValue():
            value = self.visit(ctx.attrValue())
            return (name, value)
        else:
            return (name, None)

    def visitAttrValue(self, ctx):
        if ctx.STRING_LITERAL():
            return ctx.STRING_LITERAL().getText()
        elif ctx.Number():
            return int(ctx.Number().getText())  # or float, depending on your grammar
        else:
            return ctx.Identifier().getText()

    def visitExternBlock(self, ctx):
        abi = ctx.STRING_LITERAL().getText().strip('"')
        items = [self.visit(item) for item in ctx.externItem()]
        return ExternBlock(abi, items)

    def visitExternItem(self, ctx):
        if "type" in ctx.getChild(1).getText():
            visibility = ctx.visibility().getText() if ctx.visibility() else None
            name = ctx.Identifier().getText()
            return ExternTypeDecl(name=name, visibility=visibility)

        elif "static" in ctx.getChild(0).getText():
            visibility = ctx.visibility().getText() if ctx.visibility() else None
            mutable = ctx.getChild(1).getText() == "mut"
            name = ctx.Identifier().getText()
            var_type = self.visit(ctx.type_())
            return ExternStaticVarDecl(name=name, var_type=var_type, initial_value= None, mutable=mutable, visibility=visibility)

        elif ctx.LPAREN() and ctx.RPAREN() and ctx.externParams():
            visibility = ctx.visibility().getText() if ctx.visibility() else None
            name = ctx.Identifier().getText()
            params = []
            variadic = False

            for param_ctx in ctx.externParams().externParam():
                if param_ctx.getText() == "...":
                    variadic = True
                elif param_ctx.type_():
                    type_node = self.visit(param_ctx.type_())
                    print("extern param type is ", type_node)
                    params.append(type_node)

            if str(ctx.externParams().getText()).endswith("..."):
                variadic = True

            return_type = self.visit(ctx.type_()) if ctx.type_() else None
            return ExternFunctionDecl(
                name=name,
                params=params,
                return_type=return_type,
                variadic=variadic,
                visibility=visibility
            )

        raise Exception("❌ Unsupported externItem structure")

    def visitLetStmt(self, ctx):
        var_def = self.visit(ctx.varDef())
        value = self.visit(ctx.expression()) if ctx.expression() else None
        return LetStmt(var_def, value)
    
    def visitVarDef(self, ctx):
        by_ref = False
        mutable = False
        name = None
        var_type = None

        tokens = [ctx.getChild(i).getText() for i in range(ctx.getChildCount())]

        if 'ref' in tokens:
            by_ref = True
            if 'mut' in tokens:
                mutable = True
            name_index = tokens.index('mut') + 1 if 'mut' in tokens else tokens.index('ref') + 1
            name = tokens[name_index]

        elif tokens[0] == 'mut':
            mutable = True
            name = tokens[1]
        else:
            name = tokens[0]

        if ':' in tokens:
            type_index = tokens.index(':') + 1
            var_type = self.visit(ctx.type_())

        return VarDef(name=name, mutable=mutable, by_ref=by_ref, var_type=var_type)

    def visitStaticItem(self, ctx):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        mutable = ctx.getChild(1).getText() == "mut"  # static mut ...
        name = ctx.Identifier().getText()
        var_type = self.visit(ctx.type_())
        value = self.visit(ctx.expr()) if ctx.expr() else None
        return ExternStaticVarDecl(
            name=name,
            var_type=var_type,
            mutable=mutable,
            visibility=visibility,
            initial_value=value,
        )

    def visitMutableDef(self, ctx):
        name = ctx.Identifier().getText()
        type_node = ctx.type_()
        declared_type = self.visit(type_node) if type_node else None
        return VarDef(name=name, type=declared_type, mutable=True)

    def visitImmutableDef(self, ctx):
        name = ctx.Identifier().getText()
        type_node = ctx.type_()
        declared_type = self.visit(type_node) if type_node else None
        return VarDef(name=name, type=declared_type, mutable=False)

    def visitIfStmt(self, ctx):
        condition = self.visit(ctx.expression())
        then_branch = self.visit(ctx.block(0))
        else_branch = None
        if ctx.block(1):
            else_branch = self.visit(ctx.block(1))
        return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visitAssignStmt(self, ctx):
        target_expr = ctx.expression(0)
        value_expr = ctx.expression(1)
        child = target_expr.getChild(0)

        if isinstance(child, TerminalNode):
            name_token = child.getText()
        elif hasattr(child, 'getText'):
            name_token = child.getText()
        else:
            raise Exception(f"❌ Unsupported assignment LHS node: {type(child)}")

        value = self.visit(value_expr)
        return AssignStmt(target=name_token, value=value)

    def visitForStmt(self, ctx):
        var_name = ctx.Identifier().getText()
        iterable_expr = self.visit(ctx.expression())
        body = self.visit(ctx.block())

        return ForStmt(var=var_name, iterable=iterable_expr, body=body)

    def visitBlock(self, ctx):
        stmts = []
        for stmt_ctx in ctx.statement():
            result = self.visit(stmt_ctx)
            stmts.append(result)
        return stmts
    
    def visitExpressionStatement(self, ctx):
        expr = self.visit(ctx.expression())
        return ExpressionStmt(expr=expr, line=ctx.start.line, column=ctx.start.column)

    def visitStatement(self, ctx):
        if ctx.Identifier():
            name = ctx.Identifier().getText()
            return ExpressionStmt(expr=IdentifierExpr(name=name), line=ctx.start.line, column=ctx.start.column)
        if ctx.letStmt():
            return self.visit(ctx.letStmt())
        elif ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        elif ctx.assignStmt():
            return self.visit(ctx.assignStmt())
        elif ctx.forStmt():
            return self.visit(ctx.forStmt()) 
        elif ctx.staticVarDecl():
            return self.visit(ctx.staticVarDecl())
        elif ctx.whileStmt():
            return self.visit(ctx.whileStmt())
        elif ctx.matchStmt():
            return self.visit(ctx.matchStmt())
        elif ctx.compoundAssignment():
            return self.visit(ctx.compoundAssignment())
        else:
            print("⚠️ Unknown statement:", ctx.getText())
            return None

    def visitStaticVarDecl(self, ctx):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        mutable = ctx.getChild(2).getText() == 'mut' if ctx.getChild(1).getText() == 'static' else False
        identifier_index = 3 if mutable else 2
        name = ctx.getChild(identifier_index).getText()
        var_type = None
        if ctx.type_():
            var_type = self.visit(ctx.type_())
        else:
            colon_index = [i for i, child in enumerate(ctx.children) if child.getText() == ':'][0]
            eq_index = [i for i, child in enumerate(ctx.children) if child.getText() == '='][0]
            type_tokens = ctx.children[colon_index + 1:eq_index]
            type_str = ''.join(child.getText() for child in type_tokens).strip()
            var_type = self._basic_type_from_str(type_str)

        initializer = self.visit(ctx.initializer())
        print("init val type is ", initializer.__class__)

        return StaticVarDecl(
            name=name,
            var_type=var_type,
            mutable=mutable,
            visibility=visibility,
            initial_value=initializer)

    binary_operators = {'==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '%', '&&', '||'}

    def visitExpression(self, ctx):
        text = ctx.getText()
        # print("expression is ", text)
        # print("expression is ", text, ctx.getChildCount())
        if ctx.postfixExpression() is not None:
            print("yeah!")
            return self.visit(ctx.postfixExpression())

        if ctx.getChildCount() == 3:
            middle = ctx.getChild(1)
            if isinstance(middle, TerminalNode):
                op = middle.getText()
                if op in self.binary_operators:
                    left_expr = self.visit(ctx.getChild(0))
                    right_expr = self.visit(ctx.getChild(2))
                    return BinaryExpr(left=left_expr, op=op, right=right_expr)

        elif "as" in text and ctx.getChildCount() >= 3:
            print("cast expression is ", text)
            left_expr = self.visit(ctx.expression(0))
            type_nodes = ctx.type_()
            result = left_expr
            for i in range(len(type_nodes)):
                type_node = self._basic_type_from_str(type_nodes[i].getText())
                result = CastExpr(expr=result, target_type=type_node)
            return result

        if text.isdigit():
            return LiteralExpr(value=int(text))
        if ctx.getChildCount() == 1:
            child = ctx.getChild(0)
            if isinstance(child, RustParser.RustParser.PrimaryExpressionContext):
                return IdentifierExpr(name=child.getText())

        if ctx.getChild(0).getText() == '*':
            inner_expr = self.visit(ctx.getChild(1))
            return DereferenceExpr(expr=inner_expr)

        if ctx.getChildCount() == 3 and ctx.getChild(1).getText() == 'as':
            expr = self.visit(ctx.getChild(0))
            type_text = ctx.getChild(2).getText()
            target_type = self._basic_type_from_str(type_text)
            return CastExpr(expr=expr, target_type=target_type)

        if text.startswith("'") and text.endswith("'"):
            char_value = text[1]
            return CharLiteralExpr(value=char_value)

        if ctx.primaryExpression():
            return self.visit(ctx.primaryExpression())
        try:
            float_val = float(text)
            return LiteralExpr(value=float_val)
        except ValueError:
            pass
        if text == "true":
            return BoolLiteral(True)
        elif text == "false":
            return BoolLiteral(False)
        elif text.startswith('"') and text.endswith('"'):
            return LiteralExpr(value=text[1:-1])
        elif text.startswith('[') and text.endswith(']'):
            print("sorry u saw meeeee")
            inner = text[1:-1].strip()
            if not inner:
                elements = []
            elif ';' in inner:
                value_str, size_str = [x.strip() for x in inner.split(';', 1)]
                try:
                    value_expr = LiteralExpr(value=int(value_str))
                except ValueError:
                    try:
                        value_expr = LiteralExpr(value=float(value_str))
                    except ValueError:
                        value_expr = IdentifierExpr(name=value_str)

                try:
                    repeat_expr = LiteralExpr(value=int(size_str))
                except ValueError:
                    repeat_expr = IdentifierExpr(name=size_str)

                return RepeatArrayLiteral(
                    elements=[value_expr],  # Keep 1 for semantic clarity
                    count=repeat_expr
                )
            else:
                element_texts = [e.strip() for e in inner.split(',')]
                elements = []
                for e_text in element_texts:
                    try:
                        elements.append(LiteralExpr(value=int(e_text)))
                    except ValueError:
                        try:
                            elements.append(LiteralExpr(value=float(e_text)))
                        except ValueError:
                            elements.append(IdentifierExpr(name=e_text))
                return ArrayLiteral(elements=elements)
        elif ctx.primaryExpression():
            ident = ctx.getText()
            return IdentifierExpr(ident)

        print("with sorrow: ", text, ctx.getChild(0).__class__)
        raise Exception(f"❌ Unsupported literal expression: {text}")

    def visitCharLiteralExpr(self, ctx):
        return ctx.value

    def visitPrimaryExpression(self, ctx):
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.Identifier():
            return IdentifierExpr(ctx.Identifier().getText())
        elif ctx.expression():
            return self.visit(ctx.expression())
        # elif ctx.Identifier() and ctx.argumentList():
        #     # Function call: foo(1, 2)
        #     args = self.visit(ctx.argumentList()) if ctx.argumentList() else []
        #     return FunctionCall(name=ctx.Identifier().getText(), args=args)
        else:
            raise Exception(f"❌ Unsupported primary expression: {ctx.getText()}")

    def visit_borrowExpression(self, ctx):
        expr = self.visit(ctx.expression())
        if not isinstance(expr, IdentifierExpr):
            raise Exception("Can only borrow variables (identifiers).")

        return BorrowExpr(expr.name)

    def visitType(self, ctx):
        type_str = ctx.getText()
        if type_str.startswith('[') and ';' in type_str and type_str.endswith(']'):
            inner_type_str, size_str = type_str[1:-1].split(';')
            inner_type = self._basic_type_from_str(inner_type_str.strip())  # Extract base type
            size = int(size_str.strip())  # Extract array size (e.g., 8000)
            return ArrayType(inner_type, size)

        elif type_str.startswith('[') and type_str.endswith(']'):
            inner_type_str = type_str[1:-1]
            inner_type = self._basic_type_from_str(inner_type_str.strip())  # Extract base type
            return ArrayType(inner_type, None)  # No size specified

        elif ctx.pointerType():
            return self.visit(ctx.pointerType())

        elif ctx.basicType().typePath():
            return type_str.split("::")[-1]  # Return just the type name after the last '::'

        else:
            print("Unknown type:", type_str)
            return type_str

    def visitPointerType(self, ctx):
        mut_token = ctx.getChild(1).getText()
        mutable = (mut_token == "mut")
        pointee_ctx = ctx.type_()
        pointee_type = self.visit(pointee_ctx) if pointee_ctx else None

        return PointerType(mutable, pointee_type)

    def visitPathType(self, ctx):
        return self.visit(ctx.path())

    def visitPath(self, ctx):
        segments = [seg.getText() for seg in ctx.pathSegment()]
        return PathType(segments=segments)

    def visitLiteral(self, ctx):
        print("in literal")
        text = ctx.getText()
        if text == "true":
            return BoolLiteral(True)
        elif text == "false":
            return BoolLiteral(False)
        elif ctx.Number():
            return LiteralExpr(value=int(text))
        elif ctx.arrayLiteral():
            return ArrayLiteral(ctx)

    def visitArrayLiteral(self, ctx):
        if ctx.getChildCount() == 5 and ctx.getChild(2).getText() == ';':
            value_expr = self.visit(ctx.expression(0))
            count_expr = self.visit(ctx.expression(1))
            return RepeatArrayLiteral(
                value=value_expr,
                count=count_expr,
                line=self._get_line(ctx),
                column=self._get_column(ctx))
        else:
            elements = [self.visit(expr) for expr in ctx.expression()]
            return ArrayLiteral(
                elements=elements,
                line=self._get_line(ctx),
                column=self._get_column(ctx))

    def visitInitializer(self, ctx):
        if ctx.expression():
            return self.visit(ctx.expression())
        else:
            print("Unhandled initializer kind")
            return None

    def visitWhileStmt(self, ctx):
        condition = self.visit(ctx.expression())
        body = [self.visit(stmt) for stmt in ctx.block().statement()]
        return WhileStmt(condition=condition, body=body, line=ctx.start.line, column=ctx.start.column)

    def visitMatchStmt(self, ctx):
        expr = self.visit(ctx.expression())
        arms = []
        for arm_ctx in ctx.matchArm():
            patterns = []
            for pat_ctx in arm_ctx.matchPattern():
                pat_text = pat_ctx.getText()
                patterns.append(MatchPattern(pat_text))

            body = [self.visit(stmt) for stmt in arm_ctx.block().statement()]
            arms.append(MatchArm(patterns=patterns, body=body))

        return MatchStmt(expr=expr, arms=arms, line=ctx.start.line, column=ctx.start.column)

    def visitCompoundAssignment(self, ctx):
        print("In visitCompoundAssignment")
        lhs_ctx = ctx.expression(0)
        rhs_ctx = ctx.expression(1)
        target = self.visit(lhs_ctx)
        value = self.visit(rhs_ctx)
        op = ctx.compoundOp().getText()
        return CompoundAssignment(
            target=target, op=op, value=value,
            line=ctx.start.line, column=ctx.start.column)
