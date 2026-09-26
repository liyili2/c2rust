import os
from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import setParents
from rust.commons.RustASTTransformer import RustASTTransformer
from repair.pyggi.tree.abstract_engine import AbstractTreeEngine
from rust.visitors.MarkingVisitor import MarkingVisitor

def pretty_print_ast(node, indent=0, visited=None):
    if visited is None:
        visited = set()

    lines = []
    prefix = ' ' * indent

    if isinstance(node, (str, int, float, bool, type(None))):
        return f"{prefix}{repr(node)}"

    node_id = id(node)
    if node_id in visited:
        return f"{prefix}<Cycle: {type(node).__name__}>"

    visited.add(node_id)

    if isinstance(node, list):
        for n in node:
            lines.append(pretty_print_ast(n, indent, visited))
    elif hasattr(node, '__dict__'):
        lines.append(f"{prefix}{type(node).__name__}:")
        for attr, value in vars(node).items():
            if attr == "parent":
                continue
            lines.append(f"{prefix}  {attr}:")
            lines.append(pretty_print_ast(value, indent + 4, visited))
    else:
        lines.append(f"{prefix}{repr(node)}")

    return '\n'.join(lines)

import os
from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.Printers import RustASTPrinter
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.modification.ModificationPointSelector import ModificationPointSelector
from repair.pyggi.tree.abstract_engine import AbstractTreeEngine


class RustEngine(AbstractTreeEngine):

    @classmethod
    def get_contents(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        lexer = RustLexer(InputStream(source_code))
        token_stream = CommonTokenStream(lexer)
        parser = RustParser(token_stream)
        tree = parser.program()
        transformer = RustASTTransformer()
        return transformer.visit(tree)  # unmarked AST root

    @classmethod
    def get_modification_points(cls, contents_of_file):
        # Existence check only, at load time - operators re-mark and
        # re-select fresh on every create()/apply(), since ids must reflect
        # the tree as it currently stands mid-patch, not this snapshot.
        marked = contents_of_file.accept(MarkingVisitor())
        points = ModificationPointSelector().eligible_points(marked)
        if not points:
            raise ValueError("No eligible modification points found")
        return points

    @classmethod
    def get_source(cls, program, file_name, index):
        return index.node.accept(RustASTPrinter())

    @classmethod
    def dump(cls, contents_of_file, file_name=None):
        # AbstractProgram.dump() calls engine.dump(contents, file_name) -
        # two args - even though AbstractEngine's own abstract signature
        # only declares one. Accepting file_name here matches the real
        # call site; XmlEngine/AstorEngine's single-arg dump would break
        # under that call path too, so this isn't something specific to
        # your engine - just something to be aware of.
        return contents_of_file.accept(RustASTPrinter())

    @classmethod
    def write_to_tmp_dir(cls, contents_of_file, tmp_path):
        with open(tmp_path, 'w', encoding='utf-8') as f:
            f.write(cls.dump(contents_of_file))

    @classmethod
    def do_replace(cls, program, op, new_contents, modification_points):
        # Delegate to the operator: it owns the mark/select/apply logic
        # (see RustOperator.do_apply), the same way QGen keeps that logic
        # on QGenOperator rather than on the engine.
        return op.do_apply(new_contents)

    @classmethod
    def do_insert(cls, program, op, new_contents, modification_points):
        raise NotImplementedError("RustEngine only supports replacement edits")

    @classmethod
    def do_delete(cls, program, op, new_contents, modification_points):
        raise NotImplementedError("RustEngine only supports replacement edits")


def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    return ext

def get_file_extension(file_path):
    """
    :param file_path: The path of file
    :type file_path: str
    :return: file extension
    :rtype: str
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension
