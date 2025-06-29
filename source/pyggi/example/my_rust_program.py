import os
import time
import shutil
import tempfile
import uuid
from types import SimpleNamespace as Result
from pyggi.tree.rust_engine import RustEngine
from pyggi.build.lib.pyggi.base.patch import Patch
from pyggi.tree.tree import TreeProgram
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.antlr.RustLexer   import RustLexer
from antlr4 import InputStream, CommonTokenStream
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

class MyRustProgram(TreeProgram):
    def __init__(self, path, config):
        self.config = config
        super().__init__(path, config)
        self.main_file = config["target_files"][0]

    @classmethod
    def get_engine(cls, file_name):
        if file_name.endswith(".rs"):
            return RustEngine
        raise Exception(f"No engine for {file_name}")

    def apply_patch(self, patch: Patch):
        tmp_root = os.path.join(os.getcwd(), "tmp_variants")
        os.makedirs(tmp_root, exist_ok=True)
        variant_dir = os.path.join(tmp_root, f"{os.path.basename(self.path)}_{int(time.time()*1000)}")
        shutil.copytree(self.path, variant_dir)
        variant = MyRustProgram(path=variant_dir, config=self.config)
        if hasattr(patch, "apply"):
            patch.apply(variant)
        else:
            edits = getattr(patch, "edits", getattr(patch, "_edits", []))
            for edit in edits:
                edit.apply(variant)

        return variant

    # ---------------------------------------------------------------------
    # The ONLY method LocalSearch really needs:
    # ---------------------------------------------------------------------
    def evaluate_patch(self, patch: Patch, timeout=15):
        """
        1. Apply `patch` to a temp copy of the project
        2. Run the Rust type‑checker on the main file
        3. Return a Result with .status and .fitness  (lower is better)
        """
        # workdir = patch.apply()           # temp variant dir
        # src_path = os.path.join(workdir.path, self.main_file)
        variant = self.apply_patch(patch)
        variant.trees = {}
        for file_name in variant.target_files:
            file_path = os.path.join(variant.path, file_name)
            with open(file_path, encoding="utf-8") as f:
                code = f.read()
            engine = variant.engines[file_name]
            tree = engine.get_contents(file_path)  # parses to AST
            variant.trees[file_name] = tree

        mutated_tree = variant.trees[self.main_file]
        engine = self.engines[self.main_file]
        mutated_code = engine.to_source_code(tree=mutated_tree)

        src_path = os.path.join(variant.path, self.main_file)
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(mutated_code)
        print("📝 Wrote mutated Rust code to:", src_path)

        start = time.time()

        try:
            with open(src_path, encoding="utf-8") as f:
                code = f.read()

            # --- parse -> AST ------------------------------------------------
            lexer   = RustLexer(InputStream(code))
            tokens  = CommonTokenStream(lexer)
            tree    = RustParser(tokens).program()

            transformer = Transformer()
            ast     = transformer.visit(tree)
            transformer.set_parents(ast)

            # --- type‑check --------------------------------------------------
            checker = TypeChecker()
            checker.visit(ast)
            error_cnt = checker.error_count

            status  = "SUCCESS"
        except Exception as exc:
            # Anything that crashes parsing/checking is an invalid patch
            error_cnt = None
            status = "CRASH"
            print("✖︎", exc)

        elapsed = time.time() - start

        # Prepare the object LocalSearch expects
        res = Result()
        res.elapsed_time = elapsed
        res.status  = status
        res.fitness = 1 / (error_cnt + 1)           # lower = better (0 == perfect)
        return res
