from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.Printers import RustASTPrinter


file_path = "Benchmarks/avl/avl.rs"


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
reassmbled_source = printer.visit(ast)
print(reassmbled_source)
