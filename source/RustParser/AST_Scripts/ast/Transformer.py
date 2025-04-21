from AST_Scripts.ast.Statement import LetStmt
from AST_Scripts.antlr.RustVisitor import RustVisitor
from AST_Scripts.ast.TopLevel import FunctionDef, StructDef, Attribute
from AST_Scripts.ast.Program import Program
from AST_Scripts.ast.Expression import LiteralExpr
from AST_Scripts.ast.Type import IntType, StringType

class Transformer(RustVisitor):
    def visit_Program(self, ctx):
        items = []
        for item in ctx.topLevelItem():
            result = self.visit(item)
            items.append(result)

        print("✅ program items are", items)
        return Program(items)

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

        return LetStmt(name=name, declared_type=declared_type, value=value)

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
        if text.startswith('"') and text.endswith('"'):
            return LiteralExpr(value=text[1:-1])
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


    def visitLiteralExpr(self, node):
        return self.get_literal_type(node.value)