import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.Printers import RustASTPrinter

from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.NodeCollector import NodeCollector
from rust.visitors.ASTEditor import ASTEditor
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.nodes.Expression import BinaryExpression
from rust.modification.Constraint import Constraint, ConstraintChecker
from rust.modification.ModificationPointSelector import ModificationPointSelector
from rust.modification.CandidateGenerator import ExistingValueCandidateGenerator


file_path = "./avl/avl.rs"


with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()

print("Tokenizing:")
lexer = RustLexer(InputStream(rust_code))
abc = CommonTokenStream(lexer)
print("Parsing:")
parser = RustParser(abc)
tree = parser.program()
print("Transforming:")
transformer = RustASTTransformer()
ast = transformer.visit(tree)

printer = RustASTPrinter()

print("Reassembled source (before any marking/editing):")
reassmbled_source = printer.visit(ast)
print(reassmbled_source)

# --- New architecture: mark -> select -> generate -> edit ---

print("\nMarking modification points:")
marked_ast = ast.accept(MarkingVisitor())

# Eligibility: which modification points are we willing to touch?
# Adjust/add Constraint(...) entries here as needed - see rust.modification.Constraint.
checker = ConstraintChecker([
    Constraint(BinaryExpression, "op", "+"),
])

print("Selecting one eligible modification point:")
selector = ModificationPointSelector(checker)
selected = selector.select(marked_ast)

if selected is None:
    print("No eligible modification points found - nothing to edit.")
else:
    print("Selected point:", printer.visit(selected.node))

    # Candidate pool: every other value that also satisfies the same
    # constraints, anywhere in the AST. NOTE: this is program-wide, not
    # scoped to the enclosing function - see the caveat below.
    pool = [
        m.node for m in NodeCollector(
            MarkedASTNode,
            lambda marked: checker.satisfies_any(marked.node),
        ).collect(marked_ast)
    ]
    print(f"Candidate pool size: {len(pool)}")

    generator = ExistingValueCandidateGenerator(pool)
    editor = ASTEditor(selected, generator)
    new_ast = marked_ast.accept(editor)

    print("\n=== ORIGINAL (marked) ===")
    print(printer.visit(marked_ast))

    print("\n=== MUTATED ===")
    print(printer.visit(new_ast))
