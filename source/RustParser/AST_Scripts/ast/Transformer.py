from antlr4 import TerminalNode
import re
from AST_Scripts.ast.Expression import ArrayLiteral, BinaryExpr, BoolLiteral, BorrowExpr, CastExpr, CharLiteralExpr, DereferenceExpr, FieldAccessExpr, FunctionCallExpr, IdentifierExpr, IndexExpr, IntLiteral, MethodCallExpr, ParenExpr, Pattern, PatternExpr, RepeatArrayLiteral, StrLiteral, StructLiteralExpr, StructLiteralField, UnaryExpr
from AST_Scripts.ast.Statement import AssignStmt, BreakStmt, CompoundAssignment, ContinueStmt, ExpressionStmt, ForStmt, IfStmt, LetStmt, LoopStmt, MatchArm, MatchPattern, MatchStmt, ReturnStmt, StaticVarDecl, StructLiteral, WhileStmt
from AST_Scripts.antlr.RustVisitor import RustVisitor
from AST_Scripts.ast.TopLevel import ExternBlock, ExternFunctionDecl, ExternStaticVarDecl, ExternTypeDecl, FunctionDef, InterfaceDef, StructDef, Attribute, TypeAliasDecl, UnionDef
from AST_Scripts.ast.Program import Program
from AST_Scripts.ast.Expression import LiteralExpr
from AST_Scripts.ast.Type import ArrayType, BoolType, IntType, PathType, PointerType, StringType, Type
from AST_Scripts.antlr import RustLexer, RustParser
from AST_Scripts.ast.VarDef import VarDef
from AST_Scripts.antlr import RustParser
from AST_Scripts.ast.Block import InitBlock
from AST_Scripts.ast.Func import FunctionParamList, Param

class Transformer(RustVisitor):
    def __init__(self):
        super().__init__()
        self.struct_defs = {}

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
        s = s.lstrip()
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
                if "*mut" in s:
                    return PointerType(mutability="mut", pointee_type=self._basic_type_from_str(s[4:].strip()))
                elif "*const" in s:
                    return PointerType(mutability="const", pointee_type=self._basic_type_from_str(s[6:].strip()))
        if "::" in s:
            if ';' in s:
                inner_type_str, _ = s.strip('[]').split(';', 1)
                return inner_type_str.strip().split('::')[-1]
            else:
                return s.strip().split('::')[-1]

        return s

    def _handleChainedMethodCall(self, ctx):
        text = ctx.getText()
        parts = text.split('.')
        receiver = self._expr_from_text(parts[0])
        current = receiver
        for part in parts[1:]:
            method_name = part
            args = []
            for i in range(ctx.getChildCount()):
                    print(f"Child {i}: {type(ctx.getChild(i))} → {ctx.getChild(i).getText()}")
                    args = [self.visit(child) for child in ctx.getChild(i).expression()]
                    break

            current = MethodCallExpr(receiver=current, method_name=method_name, args=args)
        return current

    def visitPostfixExpression(self, ctx):
        print("in postfix visitor")
        expr = self.visit(ctx.primaryExpression())
        i = 1
        while i < ctx.getChildCount():
            token = ctx.getChild(i).getText()

            if token == '(':
                print("1111111111")
                arg_list_ctx = ctx.getChild(i + 1)
                if hasattr(arg_list_ctx, 'expression'):
                    print("22222222222: ", arg_list_ctx.expression()[0].__class__)
                    args = [self.visit(e) for e in arg_list_ctx.expression()]
                    print("args are ", args)
                else:
                    print("33333333333")
                    args = []
                expr = MethodCallExpr(receiver=expr, method_name=None, args=args)
                i += 3

            elif token == '.':
                print("44444444444")
                next_token = ctx.getChild(i + 1)
                method_or_field = next_token.getText()
                if (i + 2 < ctx.getChildCount() and ctx.getChild(i + 2).getText() in ['(', '()']):
                    print("5555555555")
                    if ctx.getChild(i + 2).getText() == '()':
                        print("666666666666")
                        args = []
                        i += 3
                    else:
                        print("77777777777")
                        arg_list_ctx = ctx.getChild(i + 3)
                        if hasattr(arg_list_ctx, 'expression'):
                            print("88888888888")
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

    def visitInterfaceDef(self, ctx):
        name = ctx.Identifier().getText()
        functions = []
        for func_ctx in ctx.functionDef():
            func = self.visit(func_ctx)
            if func is not None:
                functions.append(func)
            else:
                print("Warning: Skipped a null functionDef during interface visit.")
        return InterfaceDef(name, functions)

    def visitTypeAlias(self, ctx):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        name = ctx.Identifier().getText()
        type = self.visit(ctx.type_())
        return TypeAliasDecl(name=name, type=type, visibility=visibility)

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

    def visitParam(self, ctx):
        is_mut = ctx.getChild(0).getText() == "mut"
        identifier = ctx.Identifier().getText()
        type_ctx = ctx.type_()
        typ = self.visit(type_ctx) if type_ctx else None
        return Param(name=identifier, typ=typ, is_mut=is_mut)

    def visitParamList(self, ctx):
        params = [self.visit(param_ctx) for param_ctx in ctx.param()]
        return FunctionParamList(params)

    def visitStructDef(self, ctx):
        name = ctx.Identifier().getText()
        fields = [self.visit(f) for f in ctx.structField()]
        field_types = {}
        for field_name, field_type in fields:
            field_types[field_name] = field_type
        self.struct_defs[name] = field_types
        return StructDef(name=name, fields=fields)

    def visitStructField(self, ctx):
        name = ctx.Identifier().getText()
        typ = self.visit(ctx.type_())
        return (name, typ)

    def visitStructLiteral(self, ctx):
        type_name = ctx.Identifier().getText()
        fields = [self.visit(field_ctx) for field_ctx in ctx.structLiteralField()]
        return StructLiteral(type_name, fields)

    def visitStructLiteralField(self, ctx):
        field_name = ctx.Identifier().getText()
        expr = self.visit(ctx.expression()) if ctx.expression() else None
        return (field_name, expr)

    def visitAttributes(self, ctx):
        return [self.visit(inner) for inner in ctx.innerAttribute()]

    def visitInnerAttribute(self, ctx):
        return self.visit(ctx.attribute())

    def visitAttribute(self, ctx):
        name = ctx.Identifier().getText()
        if ctx.attrValue():
            value = self.visit(ctx.attrValue())
            return Attribute(name=name, value=value)
        elif ctx.attrArgs():
            args = self.visit(ctx.attrArgs())
            return Attribute(name=name, args=args)
        else:
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
        condition = self.visit(ctx.expression(0))
        then_branch = self.visit(ctx.block(0))
        else_branch = None
        num_elseif = len(ctx.expression()) - 1
        current_else = None
        for i in range(num_elseif):
            elseif_condition = self.visit(ctx.expression(i + 1))
            elseif_block = self.visit(ctx.block(i + 1))
            new_if = IfStmt(condition=elseif_condition, then_branch=elseif_block)
            if current_else is None:
                current_else = new_if
            else:
                last = current_else
                while last.else_branch is not None:
                    last = last.else_branch
                last.else_branch = new_if

        if ctx.block() and len(ctx.block()) > num_elseif + 1:
            final_else_block = self.visit(ctx.block()[-1])
            if current_else:
                last = current_else
                while last.else_branch is not None:
                    last = last.else_branch
                last.else_branch = final_else_block
            else:
                else_branch = final_else_block
        else:
            else_branch = current_else
        return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visitAssignStmt(self, ctx):
        target_expr = self.visit(ctx.expression(0))
        value_expr = self.visit(ctx.expression(1))
        if isinstance(target_expr, (IdentifierExpr, FieldAccessExpr, IndexExpr, DereferenceExpr)):
            return AssignStmt(target=target_expr, value=value_expr)
        else:
            raise Exception(f"❌ Unsupported assignment LHS node: {type(target_expr)}")

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
        print("stmt is ", ctx.__class__, ctx.getText())
        if ctx.letStmt():
            return self.visit(ctx.letStmt())
        elif ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        elif ctx.structLiteral():
            print("struct literal stmt")
            return self.visit(ctx.structLiteral())
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
        elif ctx.returnStmt():
            return self.visit(ctx.returnStmt())
        elif ctx.loopStmt():
            return self.visit(ctx.loopStmt())
        elif ctx.getText() == "break;":
            return BreakStmt()
        elif ctx.getText() == "continue;":
            return ContinueStmt()
        else:
            print("⚠️ Unknown statement:", ctx.getText())
            return None
        
    def visitLoopStmt(self, ctx):
        block = self.visit(ctx.block())
        return LoopStmt(body=block)

    def visitReturnStmt(self, ctx):
        if ctx.getChildCount() == 3:
            expr = self.visit(ctx.expression())
            return ReturnStmt(expr)
        elif ctx.getChildCount() == 2:
            return ReturnStmt()
        elif ctx.Identifier():
            label_name = ctx.Identifier().getText()
            return label_name
        else:
            raise Exception("Unrecognized return statement")

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
        return StaticVarDecl(
            name=name,
            var_type=var_type,
            mutable=mutable,
            visibility=visibility,
            initial_value=initializer)

    binary_operators = {'==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '%', '&&', '||'}

    def visitExpression(self, ctx):
        print("expression is ", ctx.getText(), ctx.__class__)
        if ctx.primaryExpression():
            return self.visit(ctx.primaryExpression())

        elif ctx.mutableExpression():
            return self.visit(ctx.mutableExpression())

        elif ctx.unaryOpes():
            op = ctx.unaryOpes().getText()
            expr = self.visit(ctx.expression(0))
            return UnaryExpr(op, expr)

        elif ctx.fieldAccessPostFix():
            base = self.visit(ctx.expression(0))
            postfix = self.visit(ctx.fieldAccessPostFix())
            return FieldAccessExpr(base, postfix)

        elif ctx.booleanOps():
            left = self.visit(ctx.expression(0))
            op = ctx.booleanOps().getText()
            right = self.visit(ctx.expression(1))
            return BinaryExpr(op, left, right)

        elif ctx.binaryOps():
            left = self.visit(ctx.expression(0))
            op = ctx.binaryOps().getText()
            right = self.visit(ctx.expression(1))
            return BinaryExpr(op, left, right)

        elif ctx.conditionalOps():
            left = self.visit(ctx.expression(0))
            op = ctx.conditionalOps().getText()
            right = self.visit(ctx.expression(1))
            return BinaryExpr(op, left, right)

        elif ctx.patternSymbol():
            left = self.visit(ctx.expression(0))
            op = ctx.patternSymbol().getText()
            right = self.visit(ctx.expression(1))
            return BinaryExpr(op, left, right)

        elif ctx.compoundOps():
            left = self.visit(ctx.expression(0))
            op = ctx.compoundOps().getText()
            right = self.visit(ctx.expression(1))
            return BinaryExpr(op, left, right)

        elif ctx.castExpressionPostFix():
            expr = self.visit(ctx.expression(0))
            cast = self.visit(ctx.castExpressionPostFix())
            return CastExpr(expr, cast)

        elif ctx.callExpressionPostFix():
            return self.visit(ctx.callExpressionPostFix())

        elif ctx.parenExpression():
            return self.visit(ctx.parenExpression())

        elif ctx.structFieldDec():
            return self.visit(ctx.structFieldDec())

        elif ctx.borrowExpression():
            return self.visit(ctx.borrowExpression())

        elif ctx.dereferenceExpression():
            return self.visit(ctx.dereferenceExpression())

        elif ctx.expressionBlock():
            return self.visit(ctx.expressionBlock())

        elif ctx.patternPrefix():
            value_expr = self.visit(ctx.expression(0))
            pattern_ctx = ctx.patternPrefix().pattern()
            pattern_node = self.visit(pattern_ctx)
            return PatternExpr(value_expr, pattern_node)

        raise Exception(f"Unrecognized expression structure: {ctx.getText()}")

    def visitCallExpression(self, ctx):
        print("in call expression")
        path = [ctx.Identifier(0).getText()]
        for ident in ctx.Identifier()[1:]:
            path.append(ident.getText())
        expr_nodes = []
        if ctx.expression():
            expr_nodes.append(self.visit(ctx.expression(0)))
            for i in range(1, len(ctx.expression())):
                expr_nodes.append(self.visit(ctx.expression(i)))
        return FunctionCallExpr(path=path, arguments=expr_nodes)

    def visitPrimaryExpression(self, ctx):
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.Identifier():
            return IdentifierExpr(ctx.Identifier().getText())
        else:
            raise Exception(f"Unknown primary expression: {ctx.getText()}")

    def visitQualifiedFunctionCall(self, ctx):
        print("in qualified")
        # type_path = self.visit(ctx.typePath())
        print("path is ", ctx.Identifier().__class__ , len(ctx.Identifier()))
        function_name = ctx.Identifier().getText()
        print("name is ", function_name)
        generic_args = self.visit(ctx.genericArgs()) if ctx.genericArgs() else None
        print("args are ", generic_args)
        if ctx.argumentList():
            args = self.visit(ctx.argumentList())
        else:
            args = []

        return MethodCallExpr(method_name=function_name, args=args)

    def visitGenericArgs(self, ctx):
        return [self.visit(ty) for ty in ctx.type()]

    def visitDereferenceExpression(self, ctx):
        target_expr = self.visit(ctx.expression())
        return DereferenceExpr(target_expr)

    def visitCharLiteralExpr(self, ctx):
        return ctx.value

    def visit_borrowExpression(self, ctx):
        expr = self.visit(ctx.expression())
        if not isinstance(expr, IdentifierExpr):
            raise Exception("Can only borrow variables (identifiers).")
        return BorrowExpr(expr.name)

    def visitCastExpr(self, node):
        expr = self.visit(node.expr)
        target_type = node.type
        return CastExpr(expr=expr, type=target_type)

    def visitPattern(self, ctx):
        name = ctx.Identifier().getText() if ctx.Identifier() else "<missing>"
        return Pattern(name)

    def visitType(self, ctx):
        type_str = ctx.getText()
        # print("in visit type: ", type_str)
        if type_str.startswith('[') and ';' in type_str and type_str.endswith(']'):
            inner_type_str, size_str = type_str[1:-1].split(';')
            inner_type = self._basic_type_from_str(inner_type_str.strip())
            size = int(size_str.strip())
            return ArrayType(inner_type, size)

        elif type_str.startswith('[') and type_str.endswith(']'):
            inner_type_str = type_str[1:-1]
            inner_type = self._basic_type_from_str(inner_type_str.strip())
            return ArrayType(inner_type, None)

        elif ctx.pointerType():
            return self.visit(ctx.pointerType())

        elif "::" in type_str:
            return type_str.split("::")[-1]

        else:
            return type_str

    def visitPointerType(self, ctx):
        mut_token = ctx.getChild(1).getText()
        mutable = (mut_token == "mut")
        pointee_type_ctxs = ctx.type_()
        if isinstance(pointee_type_ctxs, list) :
            pointee_type = self.visit(pointee_type_ctxs[0]) if pointee_type_ctxs else None
        else:
            pointee_type = self.visit(pointee_type_ctxs) if pointee_type_ctxs else None

        return PointerType(mutable, pointee_type)

    def visitPathType(self, ctx):
        return self.visit(ctx.path())

    def visitPath(self, ctx):
        segments = [seg.getText() for seg in ctx.pathSegment()]
        return PathType(segments=segments)

    def visitLiteral(self, ctx):
        if ctx.arrayLiteral():
            return self.visit(ctx.arrayLiteral())
        elif ctx.booleanLiteral():
            return self.visit(ctx.booleanLiteral())
        elif ctx.HexNumber():
            return int(ctx.HexNumber().getText(), 16)
        elif ctx.Number():
            return int(ctx.Number().getText())
        elif ctx.SignedNumber():
            return int(ctx.SignedNumber().getText())
        elif ctx.BYTE_STRING_LITERAL():
            text = ctx.BYTE_STRING_LITERAL().getText()
            return bytes(text[2:-1], "utf-8")
        elif ctx.Binary():
            return int(ctx.Binary().getText(), 2)
        elif ctx.STRING_LITERAL():
            return ctx.STRING_LITERAL().getText()[1:-1]
        elif ctx.CHAR_LITERAL():
            return ctx.CHAR_LITERAL().getText()[1:-1]
        elif ctx.NONE():
            return None
        else:
            raise ValueError("Unknown literal type")

    def visitParenExpr(self, ctx):
        inner_expr = ctx.expression()
        result = self.visit(inner_expr)
        return result

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
            print("1")
            return self.visit(ctx.expression())
        elif ctx.block():
            print("2")
            return self.visit(ctx.block())
        elif ctx.initBlock():
            print("3")
            return self.visit(ctx.initBlock())
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
        lhs_ctx = ctx.expression(0)
        rhs_ctx = ctx.expression(1)
        target = self.visit(lhs_ctx)
        value = self.visit(rhs_ctx)
        op = ctx.compoundOp().getText()
        return CompoundAssignment(
            target=target, op=op, value=value,
            line=ctx.start.line, column=ctx.start.column)
