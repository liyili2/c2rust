from RustParser.AST_Scripts.antlr.RustVisitor import RustVisitor

class RustUnparser(RustVisitor):
    def visitProgram(self, ctx):
        lines = []

        for item_group in ctx.items:
            if isinstance(item_group, list):
                for item in item_group:
                    item_text = self.visit(item)
                    if item_text:
                        lines.append(item_text)
            else:
                if item_group is not None:
                    item_text = self.visit(item_group)
                    if item_text:
                        lines.append(item_text)

        return '\n\n'.join(lines)

    def generic_visit(self, node):
        print(f"[Unparser] No specific visit method for: {type(node)}")
        parts = []
        for child in getattr(node, "children", []):
            if hasattr(child, "accept"):
                parts.append(self.visit(child))
            elif hasattr(child, "getText"):
                parts.append(child.getText())
            else:
                parts.append(str(child))
        return ''.join(parts)

    def visitTopLevelItem(self, ctx):
        if ctx.function():
            return self.visit(ctx.function())
        elif ctx.structItem():
            return self.visit(ctx.structItem())
        elif ctx.useItem():
            return self.visit(ctx.useItem())
        elif ctx.interfaceDef():
            return self.visit(ctx.interfaceDef())
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

    def visit_FunctionDef(self, node):
        param_list = node.params.params if hasattr(node.params, "params") else []
        params = ', '.join(f"{param.name}: {param.typ}" for param in param_list)
        return_type = f" -> {node.return_type}" if node.return_type else ""
        body = self.visit(node.body) if hasattr(node.body, "accept") else str(node.body)
        return f"fn {node.identifier}({params}){return_type} {body}"

    def visit_StructDef(self, node):
        fields = '\n'.join(f"    {name}: {typ}," for name, typ in node.fields)
        return f"struct {node.name} {{\n{fields}\n}}"

    def visit_Attribute(self, node):
        def format_arg(arg):
            if isinstance(arg, tuple):
                if len(arg) == 2:
                    return f"{arg[0]}={arg[1]}" if arg[1] is not None else str(arg[0])
                return str(arg[0])
            return str(arg)

        args = ', '.join(format_arg(arg) for arg in node.args)
        return f"#[{node.name}({args})]" if node.args else f"#[{node.name}]"

    def visit_InterfaceDef(self, node):
        funcs = '\n'.join(self.visit(func) for func in node.functions if hasattr(func, 'accept'))
        return f"interface {node.name} {{\n{funcs}\n}}"
