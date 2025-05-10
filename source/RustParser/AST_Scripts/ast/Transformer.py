from antlr4 import TerminalNode
from AST_Scripts.ast.Expression import ArrayLiteral, BoolLiteral, BorrowExpr, IdentifierExpr, IntLiteral, StrLiteral
from AST_Scripts.ast.Statement import AssignStmt, ForStmt, IfStmt, LetStmt
from AST_Scripts.antlr.RustVisitor import RustVisitor
from AST_Scripts.ast.TopLevel import ExternBlock, ExternStaticVarDecl, ExternTypeDecl, FunctionDef, StructDef, Attribute
from AST_Scripts.ast.Program import Program
from AST_Scripts.ast.Expression import LiteralExpr
from AST_Scripts.ast.Type import ArrayType, BoolType, IntType, PointerType, StringType, Type
from AST_Scripts.antlr import RustLexer, RustParser
from AST_Scripts.ast.VarDef import VarDef
from AST_Scripts.antlr import RustParser

class Transformer(RustVisitor):
    def visit_Program(self, ctx):
        items = []
        for item in ctx.topLevelItem():
            result = self.visit(item)
            items.append(result)

        #print("✅ program items are", items)
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
        if str.__contains__(ctx.getChild(1).getText(), "type"):
            visibility = ctx.visibility().getText() if ctx.visibility() else None
            name = ctx.Identifier().getText()
            return ExternTypeDecl(name=name, visibility=visibility)

        elif str.__contains__(ctx.getChild(0).getText(), "static"):
            print(1)
            visibility = ctx.visibility().getText() if ctx.visibility() else None
            print(2)
            mutable = False
            print(3)
            if ctx.getChild(1).getText() == "mut":
                print("mut true!")
                mutable = True
            name = ctx.Identifier().getText()
            print("name is ", name)
            var_type = self.visit(ctx.type_())
            print("var_type is ", var_type)
            return ExternStaticVarDecl(name=name, var_type=var_type, mutable=mutable, visibility=visibility)

        raise Exception("❌ Unsupported externItem structure")

    def visitLetStmt(self, ctx):
        var_def = self.visit(ctx.varDef())
        value = self.visit(ctx.expression())
        if value is None:
            raise Exception(f"❌ LetStmt has no value: {ctx.getText()}")
        return LetStmt(var_def=var_def, value=value)
    
    def visitVarDef(self, ctx):
        if ctx.mutableDef():
            return self.visit(ctx.mutableDef())
        else:
            return self.visit(ctx.immutableDef())

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
            #print("🧱 Statement transformed:", result)
            stmts.append(result)
        return stmts

    def visitStatement(self, ctx):
        if ctx.letStmt():
            return self.visit(ctx.letStmt())
        elif ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        elif ctx.assignStmt():
            return self.visit(ctx.assignStmt())
        elif ctx.forStmt():
            return self.visit(ctx.forStmt())   
        else:
            print("⚠️ Unknown statement:", ctx.getText())
            return None

    #TODO : make it more clean and organized
    def visitExpression(self, ctx):
        if ctx.primaryExpression():
            return self.visit(ctx.primaryExpression())
        text = ctx.getText()
        if text.isdigit():
            return LiteralExpr(value=int(text))
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
            inner = text[1:-1].strip()
            if not inner:
                elements = []
            else:
                element_texts = [e.strip() for e in inner.split(',')]
                elements = []
                for e_text in element_texts:
                    try:
                        if e_text.isdigit():
                            elements.append(LiteralExpr(value=int(e_text)))
                        else:
                            float_val = float(e_text)
                            elements.append(LiteralExpr(value=float_val))
                    except ValueError:
                        elements.append(IdentifierExpr(e_text))
            return ArrayLiteral(elements=elements)
        elif ctx.primaryExpression():
            ident = ctx.getText()
            return IdentifierExpr(ident)
        raise Exception(f"❌ Unsupported literal expression: {text}")

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
            inner_type = self._basic_type_from_str(inner_type_str.strip())
            size = int(size_str.strip())
            return ArrayType(inner_type, size)

        elif type_str.startswith('[') and type_str.endswith(']'):
            inner_type_str = type_str[1:-1]
            inner_type = self._basic_type_from_str(inner_type_str.strip())
            return ArrayType(inner_type, None)

        return self._basic_type_from_str(type_str)

    def _basic_type_from_str(self, s: str):
        s = s.strip()

        # Check for basic types first
        if s in {"i32", "u32", "f64", "bool", "char", "usize", "isize", "FILE"}:
            return Type()

        # Handle pointer types
        if s.startswith("*mut "):
            pointee_type = self._basic_type_from_str(s[5:].strip())  # Remove "*mut " prefix and recurse
            return PointerType(mutability="mut", pointee_type=pointee_type)
        
        if s.startswith("*const "):
            pointee_type = self._basic_type_from_str(s[7:].strip())  # Remove "*const " prefix and recurse
            return PointerType(mutability="const", pointee_type=pointee_type)
        
        # Handle case for pointer types without space (e.g., "*mutFILE" or "*constFILE")
        if s.startswith("*mut") or s.startswith("*const"):
            if " " in s:  # If there’s a space, it’s a normal pointer type with a separate pointee
                pointer_type, pointee = s.split(" ", 1)
                if pointer_type == "*mut":
                    return PointerType(mutability="mut", pointee_type=self._basic_type_from_str(pointee.strip()))
                elif pointer_type == "*const":
                    return PointerType(mutability="const", pointee_type=self._basic_type_from_str(pointee.strip()))
            else:
                # Handle cases like "*mutFILE" or "*constFILE"
                if s.startswith("*mut"):
                    return PointerType(mutability="mut", pointee_type=self._basic_type_from_str(s[5:].strip()))
                elif s.startswith("*const"):
                    return PointerType(mutability="const", pointee_type=self._basic_type_from_str(s[7:].strip()))

        # Default to basic type if no match
        return Type()

    def visitPointerType(self, ctx):
        mut_token = ctx.getChild(1).getText()
        mutable = (mut_token == "mut")
        pointee_ctx = ctx.type()
        pointee_type = self.visit(pointee_ctx) if pointee_ctx else None

        return PointerType(mutable, pointee_type)

    def visitLiteral(self, ctx):
        text = ctx.getText()
        if text == "true":
            return BoolLiteral(True)
        elif text == "false":
            return BoolLiteral(False)
        elif ctx.Number():
            return LiteralExpr(value=int(text))

    def visitArrayLiteral(self, ctx):
        elements = [self.visit(expr) for expr in ctx.expression()]
        return ArrayLiteral(elements)
