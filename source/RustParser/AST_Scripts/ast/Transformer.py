from antlr4 import TerminalNode
from AST_Scripts.ast.Expression import BoolLiteral, IdentifierExpr, IntLiteral, StrLiteral
from AST_Scripts.ast.Statement import AssignStmt, IfStmt, LetStmt
from AST_Scripts.antlr.RustVisitor import RustVisitor
from AST_Scripts.ast.TopLevel import FunctionDef, StructDef, Attribute
from AST_Scripts.ast.Program import Program
from AST_Scripts.ast.Expression import LiteralExpr, VariableRef
from AST_Scripts.ast.Type import BoolType, IntType, StringType
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
        else:
            raise Exception(f"❌ Unknown literal type for value: {repr(value)}")

    def visitTopLevelItem(self, ctx):
        print("visit top level")
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

        print("let type node is", type_node)
        declared_type = self.visit(type_node) if type_node else None
        value = self.visit(ctx.expression()) if ctx.expression() else None
        if value is None:
            raise Exception(f"❌ LetStmt has no value: {ctx.getText()}")

        if type_node is None:
            declared_type = self.get_literal_type(value)
            print("let type node#2 is", declared_type)

        return LetStmt(name=name, declared_type=declared_type, value=value)

    def visitIfStmt(self, ctx):
        print("======================================visiting if stmt")
        condition = self.visit(ctx.expression())
        then_branch = self.visit(ctx.block(0))

        else_branch = None
        if ctx.block(1):  # if the optional else exists
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
            print("assignment case")
            return self.visit(ctx.assignStmt())   
        else:
            print("⚠️ Unknown statement:", ctx.getText())
            return None

    def visitExpression(self, ctx):
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
        elif ctx.primaryExpression():
            ident = ctx.getText()
            return IdentifierExpr(ident)

        raise Exception(f"❌ Unsupported literal expression: {text}")

    def visitType(self, ctx):
        type_str = ctx.getText()
        print(f"🎯 Visiting type: {type_str}")
        if type_str == "i32":
            return IntType()
        elif type_str == "String":
            return StringType()
        else:
            raise Exception(f"❌ Unknown type: {type_str}")

    def visitLiteral(self, ctx):
        text = ctx.getText()
        if text == "true":
            return BoolLiteral(True)
        elif text == "false":
            return BoolLiteral(False)
        elif ctx.Number():
            return LiteralExpr(value=int(text))
