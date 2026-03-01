from rust.ast.Expression import *
from rust.ast.Statement import *
from rust.ast.Program import *
from rust.ast.Type import *


def get_all_parents(ast_root, target_node, parent=None):
        if isinstance(parent, Program):
            return [parent]
        if parent is None and not isinstance(target_node, Program):
            parent = getattr(target_node, 'parent', None)
            if parent is None:
                raise ValueError("Target node has no parent reference")

        return [parent] + get_all_parents(ast_root, parent, parent.parent)

def _expr_from_text(self, text):
        text = text.strip()
        if text.isdigit():
            return LiteralExpression(expression=int(text))
        elif text.startswith("'") and text.endswith("'"):
            return LiteralExpression(text[1:-1])
        try:
            return LiteralExpression(expression=float(text))
        except ValueError:
            pass
        return IdentifierExpression(name=text)

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
                args = [self.visit(child) for child in ctx.getChild(i).expression()]
                break

        current = FunctionCallExpression(caller=current, callee=method_name, args=args)
    return current

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

