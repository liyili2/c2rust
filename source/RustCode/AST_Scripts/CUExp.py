import ast


class VariableDeclarationCollector(ast.NodeVisitor):
    def __init__(self):
        self.variable_declarations = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                if variable_name[0].isdigit():
                    variable_name = f"_{variable_name}"
                variable_value = generate_ocaml_code_for_expression(node.value)
                self.variable_declarations.append((variable_name, variable_value))
        self.generic_visit(node)


class CUCollector(ast.NodeVisitor):
    def __init__(self):
        self.cu_instances = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'CU':
            position = generate_ocaml_code_for_expression(node.args[0])
            inner_exp = generate_ocaml_code_for_expression(node.args[1])
            self.cu_instances.append((position, inner_exp))
        self.generic_visit(node)


def generate_ocaml_code(cu_instances, variable_declarations):
    ocaml_code = []
    ocaml_code.extend(["let () =", "  (* Variable Declarations *)"])
    for variable_name, variable_value in variable_declarations:
        ocaml_code.append(f"  let {variable_name} = {variable_value} in")
    ocaml_code.append("  (* Call CU function with the declared variables *)")
    for position, inner_exp in cu_instances:
        ocaml_code.append(f"  let _ = CU ({position}, {inner_exp}) in")
    ocaml_code.append("  ()")
    ocaml_code.append(";;")
    return ocaml_code


def generate_ocaml_code_for_expression(node):
    if isinstance(node, ast.BinOp):
        left = generate_ocaml_code_for_expression(node.left)
        op = ast.get_op_symbol(node.op)
        right = generate_ocaml_code_for_expression(node.right)
        return f"({left} {op} {right})"
    elif isinstance(node, ast.Name):
        if node.id[0].isdigit():
            return f"_{node.id}"
        return node.id
    elif isinstance(node, ast.Num):
        return str(node.n)
    else:
        # Handle other cases as needed
        return ""


# Example usage:
python_code = """
X = 2
Z = 3
CU(X, Z)
CU(3, 5)
CU(2, 2)
"""

tree = ast.parse(python_code)

variable_collector = VariableDeclarationCollector()
variable_collector.visit(tree)
variable_declarations = variable_collector.variable_declarations

cu_collector = CUCollector()
cu_collector.visit(tree)
cu_instances = cu_collector.cu_instances

ocaml_code = generate_ocaml_code(cu_instances, variable_declarations)

for line in ocaml_code:
    print(line)
