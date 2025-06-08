
import os
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.Expression import Expression
from RustParser.AST_Scripts.ast.Statement import Statement
from RustParser.AST_Scripts.ast.TopLevel import Attribute, ExternBlock, ExternFunctionDecl, FunctionDef, InterfaceDef, TopLevel, TopLevelVarDef, TypeAliasDecl
from pyggi.tree.abstract_engine import AbstractTreeEngine
from typing import List, Tuple

def pretty_print_ast(node, indent=0):
    spacer = '  ' * indent
    if isinstance(node, list):
        return '\n'.join(pretty_print_ast(n, indent) for n in node)

    if hasattr(node, '__dict__'):
        lines = [f"{spacer}{node.__class__.__name__}:"]
        for key, value in vars(node).items():
            lines.append(f"{spacer}  {key}:")
            lines.append(pretty_print_ast(value, indent + 2))
        return '\n'.join(lines)
    else:
        return f"{spacer}{repr(node)}"


class RustEngine(AbstractTreeEngine):
    def parse(self, src_code):
        lexer = RustLexer(InputStream(src_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()
        return tree  # Use your AST node visitor if needed

    def to_source_code(self, tree):
        print("reached pretty-printed ast!!")

    @classmethod
    def get_contents(cls, file_path):
        print("in rust engine get contents")
        with open(file_path, 'r') as target_file:
            source_code = target_file.read()
        lexer = RustLexer(InputStream(source_code))
        token_stream = CommonTokenStream(lexer)
        parser = RustParser(token_stream)
        tree = parser.program()
        builder = Transformer()
        ast = builder.visit_Program(tree)
        # cls.process_tree(tree)
        # print("****************", pretty_print_ast(ast))
        return ast

    @classmethod
    def process_tree(cls, tree):
        # No processing needed for now
        pass

    @classmethod
    def get_modification_points(self, ast_root):
        modification_points = []

        for item in ast_root.items:
            if isinstance(item, TopLevel):
                if isinstance(item, FunctionDef):
                    body = item.body
                    for stmt in body:
                        modification_points.extend(collect_expressions(stmt, path=[item]))
                elif isinstance(item, TopLevelVarDef):
                    if hasattr(item, 'fields'):
                        for field in item.fields:
                            modification_points.extend(collect_expressions(field, path=[item]))
                    if hasattr(item, 'type_'):
                        modification_points.extend(collect_expressions(item.type_, path=[item]))

                elif isinstance(item, ExternBlock):
                    for extern_item in item.items:
                        modification_points.extend(collect_expressions(extern_item, path=[item]))

                elif isinstance(item, Attribute):
                    for arg in item.args:
                        modification_points.extend(collect_expressions(arg, path=[item]))

                elif isinstance(item, TypeAliasDecl):
                    modification_points.extend(collect_expressions(item.type, path=[item]))

                elif isinstance(item, InterfaceDef):
                    for func in item.functions:
                        modification_points.extend(collect_expressions(func, path=[item]))

                elif isinstance(item, ExternFunctionDecl):
                    if item.return_type:
                        modification_points.extend(collect_expressions(item.return_type, path=[item]))
                    for param in item.params:
                        modification_points.extend(collect_expressions(param, path=[item]))

        return modification_points

    @classmethod
    def get_source(cls, program, file_name, index):
        pass

    @classmethod
    def write_to_tmp_dir(cls, contents_of_file, tmp_path):
        pass

    @classmethod
    def dump(cls, contents_of_file):
        pass

def get_file_extension(file_path):
    """
    :param file_path: The path of file
    :type file_path: str
    :return: file extension
    :rtype: str
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension

def collect_expressions(node, path="./", index_map=None) -> List[Tuple[str, object]]:
    if index_map is None:
        index_map = {}
    results = []

    if isinstance(node, Expression):
        results.append((path.rstrip("/"), node))

    if not hasattr(node, "__dict__"):
        return results

    node_type = type(node).__name__
    index_map.setdefault(node_type, 0)
    current_index = index_map[node_type]
    index_map[node_type] += 1

    for field_name, field_value in vars(node).items():
        full_path = f"{path}{node_type}[{current_index}]/{field_name}"

        if isinstance(field_value, Expression):
            results.append((full_path, field_value))

        elif isinstance(field_value, list):
            for i, item in enumerate(field_value):
                if isinstance(item, (Expression, Statement)):
                    results += collect_expressions(item, f"{full_path}[{i}]/", index_map)

        elif hasattr(field_value, "__dict__"):
            results += collect_expressions(field_value, f"{full_path}/", index_map)

    return results