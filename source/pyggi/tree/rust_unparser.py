from AST_Scripts.antlr.RustParser import RustParser

class RustUnparser(RustParser):
    def visitProgram(self, ctx):
        lines = []
        for item in ctx.topLevelItem():
            item_text = self.visit(item)
            if item_text:
                lines.append(item_text)
        return '\n\n'.join(lines)
    
    def visitTopLevelItem(self, ctx):
        if ctx.function():
            return self.visit(ctx.function())
        elif ctx.structItem():
            return self.visit(ctx.structItem())
        elif ctx.useItem():
            return self.visit(ctx.useItem())
        # add more cases as needed
        else:
            return
        
    def visitFunction(self, ctx):
        fn_name = ctx.IDENTIFIER().getText()
        params = self.visit(ctx.parameters()) if ctx.parameters() else ''
        body = self.visit(ctx.block())
        return f"fn {fn_name}({params}) {body}"
    
    def visitParameters(self, ctx):
        return ', '.join(self.visit(p) for p in ctx.parameter())

    def visitParameter(self, ctx):
        name = ctx.IDENTIFIER().getText()
        ty = ctx.ty().getText()
        return f"{name}: {ty}"

    def visitBlock(self, ctx):
        return '{\n' + '\n'.join(self.visit(stmt) for stmt in ctx.statement()) + '\n}'
