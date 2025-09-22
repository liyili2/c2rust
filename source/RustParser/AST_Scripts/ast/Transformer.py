
from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.Expression import ArrayDeclaration, ArrayLiteral, BasicTypeCastExpr, BinaryExpr, BoolLiteral, BorrowExpr, BoxWrapperExpr, CastExpr, CharLiteral, CharLiteralExpr, DereferenceExpr, FieldAccessExpr, FunctionCallExpr, IdentifierExpr, IndexExpr, IntLiteral, MethodCallExpr, MutableExpr, ParenExpr, Pattern, PatternExpr, QualifiedExpression, RangeExpression, RepeatArrayLiteral, SafeWrapper, StrLiteral, StructDefInit, StructLiteralExpr, StructLiteralField, TypeAccessExpr, TypePathExpression, TypePathFullExpr, UnaryExpr, UnsafeExpression
from RustParser.AST_Scripts.ast.Statement import AssignStmt, BreakStmt, CallStmt, CompoundAssignment, ConditionalAssignmentStmt, ContinueStmt, ExpressionStmt, ForStmt, IfStmt, LetStmt, LoopStmt, MatchArm, MatchPattern, MatchStmt, ReturnStmt, StructLiteral, UnsafeBlock, WhileStmt
from RustParser.AST_Scripts.antlr.RustVisitor import RustVisitor
from RustParser.AST_Scripts.ast.TopLevel import StaticVarDecl, ExternBlock, ExternFunctionDecl, ExternTypeDecl, FunctionDef, InterfaceDef, StructDef, Attribute, StructField, TopLevel, TopLevelVarDef, TypeAliasDecl, UseDecl, VarDefField
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.Expression import LiteralExpr
from RustParser.AST_Scripts.ast.Type import SafeNonNullWrapper, ArrayType, BoolType, IntType, PathType, PointerType, StringType, Type
from RustParser.AST_Scripts.ast.VarDef import VarDef
from RustParser.AST_Scripts.ast.Func import FunctionParamList, Param
from RustParser.AST_Scripts.ast.Block import Block

class Transformer(RustVisitor):
    def __init__(self):
        super().__init__()
        self.struct_defs = {}
        self._depth = 0

    def visit(self, tree):
        if isinstance(tree, list):
            return [self.visit(child) for child in tree]

        rule_name = tree.__class__.__name__.replace("Context", "")
        method_name = f"visit{rule_name}"
        visitor_fn = getattr(self, method_name, None)
        self._depth += 1

        try:
            if tree is None:
                return None

            if visitor_fn is not None:
                return visitor_fn(tree)
            else:
                return self.visitChildren(tree)
        finally:
            self._depth -= 1

    topNode = None
    def visitProgram(self, ctx):
        topNode = ctx
        items = []
        for item_ctx in ctx.topLevelItem():
            result = self.visit(item_ctx)
            items.append(result)
        return Program(items)

    def visitTopLevelDef(self, ctx):
        if ctx.functionDef():
            return self.visit(ctx.functionDef())
        elif ctx.structDef():
            return self.visit(ctx.structDef())
        elif ctx.interfaceDef():
            return self.visit(ctx.interfaceDef())
        elif ctx.topLevelVarDef():
            return self.visit(ctx.topLevelVarDef())

    def visitTopLevelVarDef(self, ctx):
        visibility = (self.visit(ctx.visibility()) if ctx.visibility() else None)
        def_kind = (ctx.defKind().getText() if ctx.defKind() else None)
        name = ctx.Identifier().getText()
        if ctx.COLON():
            type_expr = self.visit(ctx.typeExpr())
            fields = None
        else:
            type_expr = None

            fields = []
            for fld_ctx in ctx.varDefField():
                fld_visibility = (self.visit(fld_ctx.visibility()) if fld_ctx.visibility() else None)
                fld_name = fld_ctx.Identifier().getText()
                fld_type = self.visit(fld_ctx.typeExpr())
                fields.append(VarDefField(fld_name, fld_type, fld_visibility))

        node = TopLevelVarDef(
            name=name, fields=fields, type=type_expr,
            def_kind=def_kind, visibility=visibility)

        return node

    def _expr_from_text(self, text):
        # print("_expr_from_text")
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
            return s
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
                    # print(f"Child {i}: {type(ctx.getChild(i))} → {ctx.getChild(i).getText()}")
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
                    expr = FieldAccessExpr(receiver=expr, name=method_or_field)
                    i += 2
            elif token == '[':
                index_expr = self.visit(ctx.getChild(i + 1))
                expr = IndexExpr(target=expr, index=index_expr)
                i += 3
            else:
                i += 1
        return expr

    # def visitFieldAccessExpr(self, expr):
    #     print("visitFieldAccessExpr")
    #     receiver_val = self.visit(expr.receiver)
    #     field_name = self.visit(expr.primaryExpression())
    #     return field_name
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
        print("Unrecognized topLevelItem:", ctx.getText())
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
        type = self.visit(ctx.typeExpr())
        return TypeAliasDecl(name=name, type=type, visibility=visibility)

    def visitUnionDef(self, ctx):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        name = ctx.Identifier().getText()
        typ = None
        if ctx.expression():
            typ = self.visit(ctx.expression())

        fields = []
        for field_ctx in ctx.unionField():
            if field_ctx.getText() in ['{', '}', ',']:
                continue
            field_name = field_ctx.Identifier().getText()
            field_visibility = field_ctx.visibility().getText() if field_ctx.visibility() else None
            field_type = self.visit(field_ctx.typeExpr())
            fields.append((field_name, field_type, field_visibility))

        return TopLevelVarDef(name=name, type=typ ,fields=fields, visibility=visibility)

    def visitFunctionDef(self, ctx):
        name = ctx.Identifier().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        return_type = self.visit(ctx.typeExpr()) if ctx.typeExpr() else None
        body = self.visit(ctx.block())
        unsafe = False
        if ctx.unsafeModifier():
            unsafe = True
        return FunctionDef(identifier=name, params=params, return_type=return_type, body=body, unsafe=unsafe)

    def visitParam(self, ctx):
        is_mut = ctx.getChild(0).getText() == "mut"
        identifier = ctx.Identifier().getText()
        type_ctx = ctx.typeExpr()
        typ = self.visit(type_ctx) if type_ctx else None
        # print("visitParam: ", )
        return Param(name=identifier, typ=typ, mutable=is_mut)

    def visitParamList(self, ctx):
        param_list = FunctionParamList([])
        for param_ctx in ctx.param():
            param = self.visit(param_ctx)
            param.set_parent(param_list)
            param_list.params.append(param)
        return param_list

    def visitStructDef(self, ctx):
        name = ctx.Identifier().getText()
        fields = [self.visit(f) for f in ctx.structField()]
        return StructDef(name=name, fields=fields)

    def visitStructField(self, ctx):
        name_token = ctx.Identifier()
        name = name_token.getText() if name_token else "<missing>"
        typ = self.visit(ctx.typeExpr())
        vis = self.visit(ctx.visibility()) if ctx.visibility() else None
        return StructField(name, typ, vis)

    def visitStructLiteral(self, ctx):
        type_name = ctx.Identifier().getText()
        fields = [self.visit(field_ctx) for field_ctx in ctx.structLiteralField()]
        return StructLiteral(type_name, fields)

    def visitStructLiteralField(self, ctx):
        field_name = ctx.Identifier().getText()
        value = self.visit(ctx.expression()) if ctx.expression() else None
        return StructLiteralField(field_name, value)

    def visitAttributes(self, ctx):
        return [self.visit(inner) for inner in ctx.innerAttribute()]

    def visitInnerAttribute(self, ctx):
        return self.visit(ctx.attribute())

    def visitAttribute(self, ctx):
        name = ctx.Identifier().getText()
        if ctx.attrValue():
            value = self.visit(ctx.attrValue())
            return Attribute(name=name, args=value)
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
            var_type = self.visit(ctx.typeExpr())
            return StaticVarDecl(name=name, var_type=var_type, initial_value= None, mutable=mutable, visibility=visibility, isExtern=True)

        elif ctx.LPAREN() and ctx.RPAREN() and ctx.externParams():
            visibility = ctx.visibility().getText() if ctx.visibility() else None
            name = ctx.Identifier().getText()
            params = []

            for param_ctx in ctx.externParams().externParam():
                if param_ctx.typeExpr():
                    type_node = self.visit(param_ctx.typeExpr())
                    params.append(type_node)

            return_type = self.visit(ctx.typeExpr()) if ctx.typeExpr() else None
            return ExternFunctionDecl(name=name, params=params, return_type=return_type, visibility=visibility)

        raise Exception("Unsupported externItem structure")

    def visitLetStmt(self, ctx):
        var_defs = ctx.varDef()
        expressions = ctx.expression()
        init_block = ctx.initBlock()

        # case 1: let varDef = expression;
        if len(var_defs) == 1 and len(expressions) == 1 and init_block is None:
            var_def = self.visit(var_defs[0])
            expr = self.visit(expressions[0])
            return LetStmt(var_def, expr)

        # case 3: let (varDef, ...) = (expression, ...)
        elif len(var_defs) > 1 and len(expressions) > 1:
            var_defs_visited = [self.visit(vd) for vd in var_defs]
            expressions_visited = [self.visit(ex) for ex in expressions]
            return LetStmt(var_defs_visited, expressions_visited)

        else:
            raise NotImplementedError("Unsupported let statement structure")

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
            var_type = self.visit(ctx.typeExpr())
        
        return VarDef(name=name, mutable=mutable, by_ref=by_ref, var_type=var_type)

    def visitStaticItem(self, ctx):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        mutable = ctx.getChild(1).getText() == "mut"
        name = ctx.Identifier().getText()
        var_type = self.visit(ctx.typeExpr())
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
        type_node = ctx.typeExpr()
        declared_type = self.visit(type_node) if type_node else None
        return VarDef(name=name, type=declared_type, mutable=True)

    def visitImmutableDef(self, ctx):
        name = ctx.Identifier().getText()
        type_node = ctx.typeExpr()
        declared_type = self.visit(type_node) if type_node else None
        return VarDef(name=name, type=declared_type, mutable=False)

    def visitIfStmt(self, ctx):
        # Initial "if" condition and block
        condition = self.visit(ctx.expression(0))
        then_branch = self.visit(ctx.block(0))
        else_branch = None

        # Build the chain of "else if" clauses in reverse order
        n_elseif = len(ctx.expression()) - 1  # excludes the first `if` expression

        # If there is a final `else` block
        if len(ctx.block()) > n_elseif + 1:
            else_branch = self.visit(ctx.block()[-1])  # final else block

        # Build "else if" chain from last to first
        for i in reversed(range(n_elseif)):
            elseif_condition = self.visit(ctx.expression(i + 1))
            elseif_then = self.visit(ctx.block(i + 1))
            else_branch = IfStmt(condition=elseif_condition, then_branch=elseif_then, else_branch=else_branch)

        return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visitAssignStmt(self, ctx):
        value_expr = self.visit(ctx.expression(1))
        target_expr = self.visit(ctx.expression(0))
        return AssignStmt(target=target_expr, value=value_expr)

    def visitForStmt(self, ctx):
        var_name = ctx.Identifier().getText()
        iterable_expr = self.visit(ctx.expression())
        body = self.visit(ctx.block())
        return ForStmt(var=var_name, iterable=iterable_expr, body=body)

    def visitBlock(self, ctx):
        # print("visitBlock")
        stmts = []
        isUnsafe = False
        if ctx.unsafeModifier():
            isUnsafe = True
        for stmt_ctx in ctx.statement():
            result = self.visit(stmt_ctx)
            stmts.append(result)
        if isUnsafe:
            return UnsafeBlock(stmts=stmts)
        return Block(stmts=stmts, isUnsafe=False)

    def visitExprStmt(self, ctx):
        expr = self.visit(ctx.primaryExpression())
        return ExpressionStmt(expr=expr, line=ctx.start.line, column=ctx.start.column)

    def visitCallStmt(self, ctx):
        function_expr = self.visit(ctx.expression())
        postfix = ctx.callExpressionPostFix()
        if postfix.functionCallArgs():
            args_ctx = postfix.functionCallArgs().expression()
            args = [self.visit(arg) for arg in args_ctx]
        else:
            print("⚠️ callExpressionPostFix not recognized format")
            args = []
        return CallStmt(callee=function_expr, args=args)

    def visitUnsafeBlock(self, ctx):
        block = self.visit(ctx.block())
        return UnsafeBlock(block)

    def visitStatement(self, ctx):
        # print("stmt is ", ctx.__class__, ctx.getText())
        # if ctx.block():
        #     return self.visit(ctx.block())
        if ctx.letStmt():
            return self.visit(ctx.letStmt())
        elif ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        elif ctx.callStmt():
            return self.visit(ctx.callStmt())
        elif ctx.structLiteral():
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
        elif ctx.exprStmt():
            return self.visit(ctx.exprStmt())
        elif ctx.structDef():
            return self.visit(ctx.structDef())
        elif ctx.conditionalAssignmentStmt():
            return self.visit(ctx.conditionalAssignmentStmt())
        elif ctx.unsafeBlcok():
            print("unsafeBlcok case")
            return self.visitBlock(ctx.unsafeBlcok())
        else:
            print("⚠️ Unknown statement:", ctx.getText())
            return None

    def visitConditionalAssignmentStmt(self, ctx):
        cond = self.visit(ctx.block())
        if ctx.safeWrapper():
            left = self.visit(ctx.safeWrapper())
            right = self.visit(ctx.expression(0))
        else:
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
        return ConditionalAssignmentStmt(cond=cond, assignment=AssignStmt(target=left, value=right))

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
        # print("visitStaticVarDecl")
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        mutable = (ctx.getChild(1).getText() == 'mut' or ctx.getChild(2).getText() == 'mut')
        identifier_index = 3 if mutable else 2
        name = ctx.Identifier(0).getText()
        var_type = None
        if ctx.typeExpr():
            var_type = self.visit(ctx.typeExpr())
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
        # print("expression is ", ctx.getText(), ctx.__class__)
        if ctx.primaryExpression():
            return self.visit(ctx.primaryExpression())

        elif ctx.mutableExpression():
            expr = self.visit(ctx.expression(0))
            return MutableExpr(expr=expr)

        elif ctx.unaryOpes():
            op = ctx.unaryOpes().getText()
            expr = self.visit(ctx.expression(0))
            return UnaryExpr(op, expr)

        elif ctx.fieldAccessPostFix():
            # print("fieldAccessPostFix")
            base = self.visit(ctx.expression(0))
            postfix = self.visitPrimaryExpression(ctx.fieldAccessPostFix().primaryExpression())
            return FieldAccessExpr(base, postfix)

        elif ctx.binaryOps():
            op = ctx.binaryOps().getText()
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            # print("binary op is ", ctx.binaryOps().getText(), left, right)
            return BinaryExpr(op=op, left=left, right=right)

        elif ctx.rangeSymbol():
            left = self.visit(ctx.expression(0))
            op = ctx.rangeSymbol().getText()
            right = self.visit(ctx.expression(1))
            return RangeExpression(left, right)

        elif ctx.compoundOps():
            left = self.visit(ctx.expression(0))
            op = ctx.compoundOps().getText()
            right = self.visit(ctx.expression(1))
            # print("compound op is ", op)
            return BinaryExpr(op, left, right)

        elif ctx.castExpressionPostFix():
            expr = self.visit(ctx.expression(0))
            cast = self.visit(ctx.castExpressionPostFix())
            # print("cast result: ", expr, " and ", cast)
            return CastExpr(expr, cast)

        # Add caller and callee
        elif ctx.callExpressionPostFix():
            func = self.visit(ctx.expression(0))
            args = self.visit(ctx.callExpressionPostFix())
            return FunctionCallExpr(func, args, id)

        elif ctx.parenExpression():
            return self.visit(ctx.parenExpression().expression())

        elif ctx.structFieldDec():
            return self.visit(ctx.structFieldDec())

        elif ctx.borrowExpression():
            return self.visit(ctx.borrowExpression())

        elif ctx.dereferenceExpression():
            return self.visit(ctx.dereferenceExpression())

        elif ctx.expressionBlock():
            return self.visit(ctx.expressionBlock())

        elif ctx.typePathExpression():
            typePath = self.visit(ctx.typePathExpression())
            identifier = self.visit(ctx.expression(0))
            return  TypePathFullExpr(type_path=typePath, value_expr=identifier)

        elif ctx.patternPrefix():
            value_expr = self.visit(ctx.expression(0))
            pattern_ctx = ctx.patternPrefix().pattern()
            pattern_node = self.visit(pattern_ctx)
            return PatternExpr(value_expr, pattern_node)

        elif ctx.arrayDeclaration():
            return self.visit(ctx.arrayDeclaration())

        elif ctx.structLiteral():
            return self.visit(ctx.structLiteral())

        elif ctx.structDefInit():
            return self.visit(ctx.structDefInit())

        elif ctx.qualifiedExpression():
            return self.visit(ctx.qualifiedExpression())

        elif ctx.typeExpr():
            expr = self.visit(ctx.expression(0))
            typeAccess = self.visit(ctx.typeExpr())
            return TypeAccessExpr(expr=expr, typeExpr=typeAccess)

        elif ctx.unsafeExpression():
            expr = self.visit(ctx.unsafeExpression().expression())
            return UnsafeExpression(expr=expr)

        elif ctx.basicTypeCastExpr():
            basicType = self.visit(ctx.basicTypeCastExpr().typeExpr())
            typePath = self.visit(ctx.basicTypeCastExpr().typePath())
            return BasicTypeCastExpr(basicType, typePath)

        elif ctx.safeWrapper():
            return self.visit(ctx.safeWrapper())

        raise Exception(f"Unrecognized expression structure: {ctx.getText()}")

    def visitSafeWrapper(self, ctx):
        expr = self.visit(ctx.expression())
        return SafeWrapper(expr=expr)

    def visitSafeNonNullWrapper(self, ctx):
        typeExpr = self.visit(ctx.typeExpr())
        return SafeNonNullWrapper(typeExpr=typeExpr)

    def visitQualifiedExpression(self, ctx):
        expr = self.visit(ctx.expression())
        return QualifiedExpression(expr)

    def visitStructDefInit(self, ctx):
        name = ctx.Identifier().getText()
        expr = self.visit(ctx.expression())
        return StructDefInit(name, expr)

    def visitArrayDeclaration(self, ctx):
        identifier = ctx.Identifier().getText()
        force = ctx.getChild(1).getText() == "!" if ctx.getChildCount() > 1 else False
        size = int(ctx.Number().getText())
        value_expr = self.visit(ctx.expression())

        return ArrayDeclaration(
            identifier=identifier,
            force=force,
            size=size,
            value=value_expr)

    def visitCallExpressionPostFix(self, ctx):
        args_ctx = ctx.functionCallArgs()
        if args_ctx is None:
            return []
        args = []
        for expr in args_ctx.expression():
            args.append(self.visit(expr))

        return args

    # def visitCallExpression(self, ctx):
    #     print("in call expression")
        # callee = self.visit(ctx.expression(0))  # the function being called
        # postfix = ctx.callExpressionPostFix()   # the arguments (ctx)
        # args = self.visit(postfix)  # returns a list of expressions
        # print("call exp result: ", ctx.func, ctx.args)
        # return FunctionCallExpr(func=ctx.func, args=ctx.args)

    # TODO: Problematic
    def visitTypePathExpression(self, ctx):
        type_str = ctx.getText()
        return TypePathExpression(type_path=type_str.split("::") , last_type=type_str.split("::")[-1])

    def visitPrimaryExpression(self, ctx):
        # print("visitPrimaryExpression")
        if isinstance(ctx, list):
            if len(ctx) != 1:
                raise Exception(f"Expected exactly one primaryExpression, got: {len(ctx)} in {ctx}")
            ctx = ctx[0]
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.Identifier():
            return IdentifierExpr(ctx.Identifier().getText())
        else:
            raise Exception(f"Unknown primary expression: {ctx.getText()}")

    def visitQualifiedFunctionCall(self, ctx):
        # type_path = self.visit(ctx.typePath())
        function_name = ctx.Identifier().getText()
        generic_args = self.visit(ctx.genericArgs()) if ctx.genericArgs() else None
        if ctx.argumentList():
            args = self.visit(ctx.argumentList())
        else:
            args = []
        return MethodCallExpr(method_name=function_name, args=args)

    def visitGenericArgs(self, ctx):
        print("generic arg call")
        return [self.visit(ty) for ty in ctx.type()]

    def visitDereferenceExpression(self, ctx):
        target_expr = self.visit(ctx.expression())
        return DereferenceExpr(target_expr)

    def visitCharLiteralExpr(self, ctx):
        return ctx.value

    def visitBorrowExpression(self, ctx):
        mutable = ctx.getChild(1).getText() == "mut"
        expr_index = 2 if mutable else 1
        expr = self.visit(ctx.getChild(expr_index))
        mutable = isinstance(expr, MutableExpr)
        return BorrowExpr(expr=expr, mutable=mutable)

    def visitCastExpr(self, node):
        expr = self.visit(node.expr)
        target_type = self.visit(node.type)
        return CastExpr(expr=expr, type=target_type)

    def visitPattern(self, ctx):
        ids = []
        for id in ctx.Identifier():
            ids.append(id.getText())
        return Pattern(ids)

    def visitTypeExpr(self, ctx):
        type_str = ctx.getText()
        if ctx.basicType():
            return self.visit(ctx.basicType())

        elif type_str.startswith('[') and ';' in type_str and type_str.endswith(']'):
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

        # elif "::" in type_str:
        #     return TypePathExpression(type_path=type_str.split("::") , last_type=type_str.split("::")[-1])
        elif str.__eq__(type_str,"i32"):
            return IntType()
        elif str.__eq__(type_str,"String"):
            return StringType()
        else:
            return type_str

    def visitBasicType(self, ctx):
        type_str = ctx.getText()
        if ctx.safeNonNullWrapper():
            print(self.visit(ctx.safeNonNullWrapper()).__class__ )
            return self.visit(ctx.safeNonNullWrapper())

        elif ctx.typePath():
            type_str = ctx.typePath().getText()
            return TypePathExpression(type_path=type_str.split("::") , last_type=type_str.split("::")[-1])
        else:
            return type_str

    def visitPointerType(self, ctx):
        mut_token = ctx.getChild(1).getText()
        mutable = (mut_token == "mut")
        pointee_type_ctxs = ctx.typeExpr()
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
        # print("visitLiteral")
        if ctx.arrayLiteral():
            return self.visit(ctx.arrayLiteral())
        elif ctx.booleanLiteral():
            return BoolLiteral(self.visit(ctx.booleanLiteral()))
        elif ctx.HexNumber():
            return int(ctx.HexNumber().getText(), 16)
        elif ctx.Number():
            # print("ctx.Number", ctx.Number().getText())
            return IntLiteral(ctx.Number().getText())
        elif ctx.SignedNumber():
            return IntLiteral(int(ctx.SignedNumber().getText()))
        elif ctx.BYTE_STRING_LITERAL():
            text = ctx.BYTE_STRING_LITERAL().getText()
            return bytes(text[2:-1], "utf-8")
        elif ctx.Binary():
            return int(ctx.Binary().getText(), 2)
        elif ctx.STRING_LITERAL():
            return StrLiteral(ctx.STRING_LITERAL().getText()[1:-1])
        elif ctx.CHAR_LITERAL():
            return CharLiteral(ctx.CHAR_LITERAL().getText()[1:-1])
        elif ctx.byteLiteral():
            return self.visit(ctx.byteLiteral())
        elif ctx.NONE():
            return None
        else:
            raise ValueError("Unknown literal type")

    def visitByteLiteral(self, ctx):
        return LiteralExpr(value=ctx.getText())

    def visitParenExpr(self, ctx):
        inner_expr = ctx.expression()
        result = self.visit(inner_expr)
        return result

    def visitArrayLiteral(self, ctx):
        # print("in array literal visitor")
        name = ""
        if ctx.Identifier():
            name = ctx.Identifier().getText()
            if ctx.expression(0):
                index_exprs = [self.visit(ctx.expression(0))]
                if ctx.expression(1):
                    index_exprs += [self.visit(expr) for expr in ctx.expression()[1:]]
                return ArrayLiteral(
                    name=IdentifierExpr(name=name),
                    elements=index_exprs)
        
        element_exprs = [self.visit(expr) for expr in ctx.expression()]
        return ArrayLiteral(name=name, elements=element_exprs)

        # else:  # Case: [value; size] constructor
        #     value = self.visit(ctx.expression(0))
        #     size = self.visit(ctx.expression(1))
        #     return ArrayConstructor(value=value, size=size)

    def visitInitializer(self, ctx):
        if ctx.expression():
            # print("1")
            return self.visit(ctx.expression())
        elif ctx.block():
            # print("2")
            return self.visit(ctx.block())
        else:
            print("Unhandled initializer kind")
            return None

    def visitWhileStmt(self, ctx):
        condition = self.visit(ctx.expression())
        body = [self.visit(stmt) for stmt in ctx.block().statement()]
        return WhileStmt(condition=condition, body=body, line=ctx.start.line, column=ctx.start.column)

    def visitMatchStmt(self, ctx):
        expr = self.visit(ctx.expression())
        arms = [self.visit(arm_ctx) for arm_ctx in ctx.matchArm()]
        return MatchStmt(expr=expr, arms=arms, line=ctx.start.line, column=ctx.start.column)

    def visitMatchArm(self, ctx):
        patterns = [self.visit(pat_ctx) for pat_ctx in ctx.matchPattern()]
        # print("patterns are ", patterns, len(patterns), ctx.block())
        body = self.visit(ctx.block())
        return MatchArm(patterns=patterns, body=body)

    def visitMatchPattern(self, ctx):
        if ctx.Number():
            return MatchPattern(int(ctx.Number().getText()))
        elif ctx.UNDERSCORE():
            return MatchPattern('_')
        elif ctx.Identifier():
            return MatchPattern(ctx.Identifier().getText())
        elif ctx.byteLiteral():
            return self.visit(ctx.byteLiteral())
        else:
            raise ValueError("Unknown matchPattern type")

    def visitCompoundAssignment(self, ctx):
        lhs_ctx = ctx.expression(0)
        rhs_ctx = ctx.expression(1)
        target = self.visit(lhs_ctx)
        value = self.visit(rhs_ctx)
        op = ctx.compoundOp().getText()
        return CompoundAssignment(
            target=target, op=op, value=value,
            line=ctx.start.line, column=ctx.start.column)

    # def visitUnionDef(self, ctx):
    #     visibility = ctx.visibility().getText() if ctx.visibility() else None
    #     name = ctx.Identifier().getText()
    #     if ctx.typeExpr():
    #         typ = self.visit(ctx.type())
    #         value = self.visit(ctx.expression())
    #         return TopLevelVarDef(visibility=visibility, name=name, type=typ, value=value)
    #     else:
    #         fields = [self.visit(field) for field in ctx.unionField()]
    #         return TopLevelVarDef(visibility=visibility, name=name, fields=fields, type=None)

    def visitConstDef(self, ctx):
        return self._visit_simple_definition(ctx, TopLevelVarDef)

    def visitUnsafeDef(self, ctx):
        return self._visit_simple_definition(ctx, TopLevelVarDef)

    def _visit_simple_definition(self, ctx, node_type):
        visibility = ctx.visibility().getText() if ctx.visibility() else None
        name = ctx.Identifier().getText()
        typ = self.visit(ctx.typeExpr())
        value = self.visit(ctx.expression())
        return node_type(visibility=visibility, name=name, type=typ, fields=value)

    def visitUseDecl(self, ctx):
        paths = [self.visit(tp) for tp in ctx.typePath()]
        identifiers = ctx.Identifier()
        aliases = [id_.getText() for id_ in identifiers] if identifiers else [None] * len(paths)

        while len(aliases) < len(paths):
            aliases.append(None)

        return UseDecl(paths, aliases)

def setParents(node, parent=None, top_level_prog=None):
    # print("setParents ", node.__class__)
    if not isinstance(node, ASTNode):
        return

    if isinstance(node, Program):
        top_level_prog = node

    if isinstance(node, FunctionDef) and isinstance(parent, InterfaceDef):
        node.parent = parent
    elif isinstance(node, TopLevel) and top_level_prog:
        node.parent = top_level_prog
    elif parent is not None:
        node.parent = parent

    for attr, value in vars(node).items():
        if attr == "parent":
            continue

        if isinstance(value, list):
            for item in value:
                setParents(item, node, top_level_prog)
        elif isinstance(value, ASTNode):
            setParents(value, node, top_level_prog)
