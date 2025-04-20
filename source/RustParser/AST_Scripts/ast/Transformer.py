from AST_Scripts.ast.Statement import LetStmt
from AST_Scripts.antlr.RustVisitor import RustVisitor
from AST_Scripts.ast.TopLevel import FunctionDef, StructDef, Attribute
from AST_Scripts.ast.Program import Program

class Transformer(RustVisitor):
    def visit_Program(self, ctx):
        print("ctx is ", len(ctx.topLevelItem()))
        print("visit program")
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
        declared_type = self.visit(ctx.type_()) if ctx.type_() else None
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
        # Add other statement types here
        else:
            print("⚠️ Unknown statement:", ctx.getText())
            return None

    def visitExpression(self, ctx):
        print("🧠 Visiting expression:", ctx.getText())
        return ctx.getText()  # or a proper AST node
