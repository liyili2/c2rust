import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import pytest
import subprocess
from antlr4 import InputStream, CommonTokenStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

class TestBstRustSuite:
    def test_rust_functional_tests(self):
        """Runs the original Rust tests using `cargo test`."""
        result = subprocess.run(["cargo", "test"], capture_output=True, text=True)
        print(result.stdout)
        assert result.returncode == 0, f"Cargo test failed:\n{result.stderr}"

    def test_type_checker_on_bst(self):
        """Runs the custom type checker on bst.rs."""
        file_path = os.path.join(os.path.dirname(__file__), "bst.rs")
        with open(file_path, "r", encoding="utf-8") as f:
            rust_code = f.read()

        lexer = RustLexer(InputStream(rust_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()

        builder = Transformer()
        custom_ast = builder.visit_Program(tree)

        checker = TypeChecker()
        checker.visit(custom_ast)
        print("Fitness eval: ", 1 / (checker.error_count + 1))

        assert checker.error_count < 10, f"Type checker found {checker.error_count} errors"
