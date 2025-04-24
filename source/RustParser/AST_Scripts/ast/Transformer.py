from antlr4 import TerminalNode
from AST_Scripts.ast.Expression import ArrayLiteral, BoolLiteral, IdentifierExpr, IntLiteral, StrLiteral
from AST_Scripts.ast.Statement import AssignStmt, ForStmt, IfStmt, LetStmt
from AST_Scripts.antlr.RustVisitor import RustVisitor
from AST_Scripts.ast.TopLevel import FunctionDef, StructDef, Attribute
from AST_Scripts.ast.Program import Program
from AST_Scripts.ast.Expression import LiteralExpr, VariableRef
from AST_Scripts.ast.Type import ArrayType, BoolType, IntType, StringType
from RustParser.AST_Scripts.antlr import RustLexer

class Transformer(RustVisitor):
    def visit_Program(self, ctx):
        items = []
        for item in ctx.topLevelItem():
            result = self.visit(item)
            items.append(result)

        print("✅ program items are", items)
        return Program(items)

    def get_literal_type(self, value):
        print("value class is ", value.__class__)
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
        if ctx.functionDef():
            return self.visit(ctx.functionDef())
        elif ctx.structDef():
            return self.visit(ctx.structDef())
        elif ctx.attribute():
            return self.visit(ctx.attribute())
        else:
            print("⚠️ Unknown topLevelItem:", ctx.getText())
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

    def visitAttribute(self, ctx):
        attr_name = ctx.attrInner().Identifier(0).getText()
        args = [i.getText() for i in ctx.attrInner().Identifier()[1:]]
        return Attribute(name=attr_name, args=args)

    def visitLetStmt(self, ctx):
        print("🧪 Visiting letStmt:", ctx.getText())
        name_tok = ctx.Identifier()
        if name_tok is None:
            raise Exception(f"❌ Could not find variable name in letStmt: {ctx.getText()}")

        name = name_tok.getText()
        type_node = ctx.type_()

        declared_type = self.visit(type_node) if type_node else None
        value = self.visit(ctx.expression()) if ctx.expression() else None
        print("-----------------------------", value)
        if value is None:
            raise Exception(f"❌ LetStmt has no value: {ctx.getText()}")

        if type_node is None:
            declared_type = self.get_literal_type(value)

        return LetStmt(name=name, declared_type=declared_type, value=value)

    def visitIfStmt(self, ctx):
        print("🔍 ifStmt text:", ctx.getText())
        condition = self.visit(ctx.expression())
        print("((((((((()))))))", condition)
        then_branch = self.visit(ctx.block(0))
        else_branch = None
        if ctx.block(1):
            else_branch = self.visit(ctx.block(1))
        return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visitAssignStmt(self, ctx):
        print("🔧 Visiting assignmentStmt:", ctx.getText())
        target_expr = ctx.expression(0)
        value_expr = ctx.expression(1)
        child = target_expr.getChild(0)

        if isinstance(child, TerminalNode):  # It's a terminal node
            name_token = child.getText()
        elif hasattr(child, 'getText'):  # Could be Identifier wrapped in primaryExpression
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
            print("🧱 Statement transformed:", result)
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

    def visitType(self, ctx):
        type_str = ctx.getText()
        print(f"🎯 Visiting type: {type_str}")

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

    def _basic_type_from_str(self, s):
        if s == "i32":
            return IntType()
        elif s == "String":
            return StringType()
        elif s == "bool":
            return BoolType()
        else:
            raise Exception(f"❌ Unknown basic type: {s}")
        
    def visitLiteral(self, ctx):
        text = ctx.getText()
        if text == "true":
            return BoolLiteral(True)
        elif text == "false":
            return BoolLiteral(False)
        elif ctx.Number():
            return LiteralExpr(value=int(text))

    def visitArrayLiteral(self, ctx):
        print("🔍 Visiting array literal:", ctx.getText())
        elements = [self.visit(expr) for expr in ctx.expression()]
        return ArrayLiteral(elements)
