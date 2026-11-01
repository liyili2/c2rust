import sys
import os
import io
import random
import argparse
import contextlib
import importlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust.visitors.Printers import RustASTPrinter
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.nodes.TopLevel import FunctionDefinition
from rust.modification.Constraint import Constraint, ConstraintChecker
from rust.modification.ModificationPointSelector import ModificationPointSelector

# Usage:  python testing.py [rust_file] [--seed N] [--test-command CMD] [--evaluate] [--ga]
#   rust_file       Rust source to mutate (default ./avl/avl.rs). Its folder is the PyGGI
#                   project folder and its file name the target file.
#   --seed N        no seed -> a random one (printed, so the run can be reproduced)
#   --test-command  command PyGGI runs in the tmp variant of the project (default: cargo test)
#   --evaluate      also run the tests on each result and print its fitness
#   --ga            also run a small jMetal genetic algorithm (implies --evaluate)
arg_parser = argparse.ArgumentParser(description="Mutation / crossover test on one Rust file")
arg_parser.add_argument("rust_file", nargs="?", default="./avl/avl.rs")
arg_parser.add_argument("--seed", type=int, default=None)
arg_parser.add_argument("--test-command", default="cargo test")
arg_parser.add_argument("--evaluate", action="store_true")
arg_parser.add_argument("--ga", action="store_true")
args = arg_parser.parse_args()

if args.seed is None:
    seed = random.randrange(2 ** 32)
    print(f"seed = {seed}")          # only when random, so the run can be repeated
else:
    seed = args.seed
file_path = args.rust_file


def quiet():
    """Silence the progress prints of the repair framework while it works."""
    return contextlib.redirect_stdout(io.StringIO())


def _find_package():
    """Dotted name of the folder holding cprogram.py (searched below this file's parent dir)."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    skip = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 'tmp_variants', 'saved_variants'}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip]
        if 'cprogram.py' in files:
            missing = [f for f in ('rpatch.py', 'rprogram.py', 'rproblem.py', 'rmutation.py',
                                   'rcrossover.py') if f not in files]
            if missing:
                raise SystemExit(f"Found cprogram.py in {dirpath}\n"
                                 f"Copy these files into that folder first: {', '.join(missing)}")
            return os.path.relpath(dirpath, root).replace(os.sep, '.')
    raise SystemExit("Could not find cprogram.py below " + root + " - set PACKAGE by hand.")


PACKAGE = __package__ or _find_package()


def _load(module, name):
    return getattr(importlib.import_module(f"{PACKAGE}.{module}"), name)


RProgram = _load("rprogram", "RProgram")
RProblem = _load("rproblem", "RProblem")
RustSwapOperator = _load("operators", "RustSwapOperator")
RustReplacementOperator = _load("operators", "RustReplacementOperator")
RustMutation = _load("rmutation", "RustMutation")
RustSubtreeCrossover = _load("rcrossover", "RustSubtreeCrossover")
strip_marks_tree = _load("operators", "strip_marks_tree")

# Eligibility: any marked expression, but only inside unsafe functions.
unsafe_functions = ConstraintChecker([
    Constraint(FunctionDefinition, "is_unsafe", True),
])

printer = RustASTPrinter()
rng = random.Random(seed)

# PyGGI project = the folder of the given file; target file = its name inside that folder.
project_dir = os.path.dirname(file_path) or "."
config = {"target_files": [os.path.basename(file_path)], "test_command": args.test_command}

# --------------------------------------------------------------------------
# Build everything. Every edit gets its own, distinct parents:
#   mutation   : mutation_parent                      -> mutant
#   crossover  : crossover_parent_1, crossover_parent_2 -> child_1, child_2
# --------------------------------------------------------------------------
with quiet():
    program = RProgram(project_dir, config=config)
    program.operators = [RustSwapOperator, RustReplacementOperator]
    problem = RProblem(program, scope_checker=unsafe_functions, rng=rng)
    mutation = RustMutation(probability=1.0, operators=program.operators,
                            scope_checker=unsafe_functions, rng=rng)
    crossover = RustSubtreeCrossover(probability=1.0, scope_checker=unsafe_functions, rng=rng)

    mutation_parent = problem.create_solution()
    mutant = mutation.execute(mutation_parent.clone())

    crossover_parent_1 = problem.create_solution()
    crossover_parent_2 = problem.create_solution()
    child_1, child_2 = crossover.execute([crossover_parent_1, crossover_parent_2])


def source(patch):
    return patch.get_ast().accept(printer)


def banner(title):
    print(f"\n===== {title} =====")


# --------------------------------------------------------------------------
# Mutation
# --------------------------------------------------------------------------
banner("AST BEFORE MUTATION")
print(source(mutation_parent))

banner("AST AFTER MUTATION")
print(source(mutant))

banner("MUTATION SUMMARY")
if len(mutant) == len(mutation_parent):
    print("No mutation applied (nothing eligible, or the edit could not be applied).")
else:
    edit = mutant.edit_list[-1]
    target_file = getattr(edit, "target_file", None) or edit._target[0]
    marked = strip_marks_tree(mutation_parent.ast[target_file]).accept(MarkingVisitor())
    points = {pt.get_id(): pt for pt in ModificationPointSelector(
        scope_checker=unsafe_functions, rng=random.Random(0)).eligible_points(marked)}
    print("Operator    :", type(edit).__name__)
    print("Selection   :", " -> ".join(mutation.last_trace))

    if hasattr(edit, "point_a_id"):                       # swap: two nodes trade places
        pa, pb = points.get(edit.point_a_id), points.get(edit.point_b_id)
        if pa is None or pb is None:
            print("Swap applied, but its two nodes could not be looked up in the parent.")
        else:
            text_a = strip_marks_tree(pa.node).accept(printer)
            text_b = strip_marks_tree(pb.node).accept(printer)
            print("Chosen nodes:", type(pa.node).__name__, "<->", type(pb.node).__name__)
            print("Node 1 before:", text_a)
            print("       after :", text_b)
            print("Node 2 before:", text_b)
            print("       after :", text_a)
    else:                                                 # replacement: one node -> candidate
        point = points.get(edit.modification_point_id)
        if point is None:
            print("Replacement applied, but its node could not be looked up in the parent.")
        else:
            print("Chosen node :", type(point.node).__name__)
            print("Before      :", strip_marks_tree(point.node).accept(printer))
            print("After       :", strip_marks_tree(edit.target).accept(printer))

# --------------------------------------------------------------------------
# Crossover
# --------------------------------------------------------------------------
banner("AST BEFORE CROSSOVER")
print("--- parent 1 ---")
print(source(crossover_parent_1))
print("--- parent 2 ---")
print(source(crossover_parent_2))

banner("AST AFTER CROSSOVER")
print("--- child 1 ---")
print(source(child_1))
print("--- child 2 ---")
print(source(child_2))

banner("CROSSOVER SUMMARY")
exchange = crossover.last_exchange
if exchange is None:
    print("No crossover applied (no compatible pair of nodes found).")
else:
    text_1 = exchange["node_a"].accept(printer)   # the node taken from parent 1
    text_2 = exchange["node_b"].accept(printer)   # the node taken from parent 2
    applied_1, applied_2 = exchange["applied"]
    print("Chosen nodes:", exchange["node_type"], "<->", exchange["node_type"])
    print("Parent 1 node before:", text_1)
    print("                after:", text_2 if applied_1 else text_1 + "   (not applied)")
    print("Parent 2 node before:", text_2)
    print("                after:", text_1 if applied_2 else text_2 + "   (not applied)")

# --------------------------------------------------------------------------
# Optional: evaluation / GA (only with --evaluate / --ga)
# --------------------------------------------------------------------------
if args.evaluate or args.ga:
    banner("FITNESS")
    for label, patch in [("mutation parent", mutation_parent), ("mutant", mutant),
                         ("crossover parent 1", crossover_parent_1),
                         ("crossover parent 2", crossover_parent_2),
                         ("child 1", child_1), ("child 2", child_2)]:
        with quiet():
            problem.evaluate(patch)
        print(f"{label}: {patch.fitness}")

if args.ga:
    from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
    from jmetal.operator.selection import BinaryTournamentSelection
    from jmetal.util.termination_criterion import StoppingByEvaluations

    with quiet():
        algorithm = GeneticAlgorithm(
            problem=problem, population_size=10, offspring_population_size=10,
            mutation=mutation, crossover=crossover, selection=BinaryTournamentSelection(),
            termination_criterion=StoppingByEvaluations(max_evaluations=100))
        algorithm.run()
        best = algorithm.result() if hasattr(algorithm, "result") else algorithm.get_result()
        best = best[0] if isinstance(best, list) else best
    banner("GA BEST")
    print("fitness:", best.fitness)
    print(source(best))