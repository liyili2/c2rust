from antlr4 import *
from RustLexer import RustLexer
from RustParser import RustParser
import os

def parse_rust_file(file_path: str, output_dir: str = "./antlr_generated/"):
    with open(file_path, encoding='utf-8') as f:
        input_text = f.read()

    i_stream = InputStream(input_text)
    lexer = RustLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = RustParser(t_stream)
    tree = parser.program()

    base_name = os.path.basename(file_path)
    output_file = os.path.join(output_dir, base_name + ".txt")
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("Here's the parsing result:\n")
        f.write(tree.toStringTree(recog=parser))

    print(f"✅ Parsed {file_path} -> {output_file}")

def main():
    base_dir = "../../../../c2safeRust_examples/"
    test_files = [
        "aggregate.rs",
        "bst.rs",
        "output.rs"
    ]

    for file_name in test_files:
        file_path = os.path.join(base_dir, file_name)
        parse_rust_file(file_path)

if __name__ == "__main__":
    main()
