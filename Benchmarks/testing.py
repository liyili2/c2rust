import sys
import os
import io
import random
import argparse
import contextlib
import importlib
import difflib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust.visitors.Printers import RustASTPrinter
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.nodes.TopLevel import FunctionDefinition
from rust.modification.Constraint import Constraint, ConstraintChecker
from rust.modification.ModificationPointSelector import ModificationPointSelector

# Usage:  python testing.py [rust_file] [--ga] [--dry-run] [--seed N] [--population N]
#                           [--generations N] [--ga-class C] [--pair-check P]
#                           [--test-command CMD] [--evaluate]
#
#   rust_file       Rust source to mutate (default ./avl/avl.rs). Its folder is the PyGGI
#                   project folder and its file name the target file.
#   (no --ga)       prints the original AST, then one mutation and one crossover
#   --ga            prints the original AST, then follows it through the Repaired GA pipeline:
#                   selection -> crossover -> mutation (swap / replacement) -> evaluation -> survival
#   --dry-run       no test command: a FAKE fitness (number of source lines changed compared
#                   with the original) is used, only to watch the pipeline run
#   --population N  population (= offspring) size for --ga, even number (default 4)
#   --generations N number of generations for --ga (default 2)
#   --ga-class      repaired | logging | topk (default topk, the last of the chain;
#                   every one is a RepairedGeneticAlgorithm)
#   --pair-check P  which nodes may be swapped / exchanged together (see pairchecker.py):
#                   none | function | function+type   (default function+type)
#   --seed N        no seed -> a random one (printed, so the run can be reproduced)
#   --test-command  command PyGGI runs in the tmp variant of the project (default: cargo test)
#   --evaluate      (without --ga) also run the tests on each result and print its fitness
arg_parser = argparse.ArgumentParser(description="Mutation / crossover / Repaired GA on one Rust file")
arg_parser.add_argument("rust_file", nargs="?", default="./avl/avl.rs")
arg_parser.add_argument("--seed", type=int, default=None)
arg_parser.add_argument("--test-command", default="cargo test")
arg_parser.add_argument("--evaluate", action="store_true")
arg_parser.add_argument("--ga", action="store_true")
arg_parser.add_argument("--dry-run", action="store_true")
arg_parser.add_argument("--population", type=int, default=4)
arg_parser.add_argument("--generations", type=int, default=2)
arg_parser.add_argument("--ga-class", default="topk", choices=["repaired", "logging", "topk"])
arg_parser.add_argument("--pair-check", default="function+type",
                        choices=["none", "function", "function+type"])
args = arg_parser.parse_args()
if args.population < 2 or args.population % 2:
    arg_parser.error("--population must be an even number >= 2 (crossover makes 2 children per pair)")

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
                                   'rcrossover.py', 'repairedga.py', 'pairchecker.py') if f not in files]
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
SameFunction = _load("pairchecker", "SameFunction")
SameNodeType = _load("pairchecker", "SameNodeType")
AllOf = _load("pairchecker", "AllOf")

# Which pairs of nodes may be swapped (mutation) or exchanged (crossover) together.
# Without a rule a swap can move a node into another function, where its variables do not exist.
if args.pair_check == "none":
    pair_checker = None
elif args.pair_check == "function":
    pair_checker = SameFunction()
else:
    pair_checker = AllOf(SameFunction(), SameNodeType())

# Eligibility: any marked expression, but only inside unsafe functions.
unsafe_functions = ConstraintChecker([
    Constraint(FunctionDefinition, "is_unsafe", True),
])

printer = RustASTPrinter()
rng = random.Random(seed)

# PyGGI project = the folder of the given file; target file = its name inside that folder.
project_dir = os.path.dirname(file_path) or "."
config = {"target_files": [os.path.basename(file_path)], "test_command": args.test_command}
target = config["target_files"][0]

# --------------------------------------------------------------------------
# Build the program (this parses the file and transforms it into the AST)
# --------------------------------------------------------------------------
with quiet():
    program = RProgram(project_dir, config=config)
    program.operators = [RustSwapOperator, RustReplacementOperator]

    if args.dry_run:
        # Replace the test run by a fake fitness: how many source lines differ from the
        # original. It means nothing for repair (the GA will favour changing little);
        # it only gives the algorithm numbers to work with, with no test command.
        CResult = _load("cresult", "CResult")
        _fake_original = program.contents[target].accept(printer).splitlines()

        def fake_evaluate_solution(patch, test_command):
            new_lines = patch.get_ast(target).accept(printer).splitlines()
            changed = sum(1 for line in difflib.unified_diff(_fake_original, new_lines,
                                                             lineterm="", n=0)
                          if line[:1] in "+-" and line[:3] not in ("+++", "---"))
            return CResult("SUCCESS", changed)

        program.evaluate_solution = fake_evaluate_solution

    problem = RProblem(program, scope_checker=unsafe_functions, pair_checker=pair_checker, rng=rng)
    # TODO: discuss the mutation probability
    mutation = RustMutation(probability=1.0, operators=program.operators,
                            scope_checker=unsafe_functions, pair_checker=pair_checker, rng=rng)
    crossover = RustSubtreeCrossover(probability=1.0, scope_checker=unsafe_functions,
                                     pair_checker=pair_checker, rng=rng)


def source(patch):
    return patch.get_ast(target).accept(printer)


def banner(title):
    print(f"\n===== {title} =====")


original_source = program.contents[target].accept(printer)
original_lines = original_source.splitlines()

banner("ORIGINAL AST (after transformation)")
print(original_source)

# ==========================================================================
# --ga : follow the AST through the Repaired GA pipeline
# ==========================================================================
if args.ga:
    import logging
    from jmetal.operator.selection import BinaryTournamentSelection
    from jmetal.util.termination_criterion import StoppingByEvaluations

    logging.getLogger("jmetal").setLevel(logging.WARNING)    # hide jMetal's [DEBUG] lines

    def short(text, width=110):
        return text if len(text) <= width else text[:width - 3] + "..."

    def edit_names(patch):
        names = [type(edit).__name__.replace("Rust", "").replace("Operator", "")
                 for edit in patch.edit_list]
        return ", ".join(names) if names else "none"

    def changes_vs_original(patch, max_lines=6):
        """The changed lines of the patch's source compared with the original program."""
        new_lines = source(patch).splitlines()
        diff = [line for line in difflib.unified_diff(original_lines, new_lines, lineterm="", n=0)
                if not line.startswith(("---", "+++"))]
        shown = diff[:max_lines]
        if len(diff) > len(shown):
            shown.append(f"... ({len(diff) - len(shown)} more changed lines)")
        return shown

    def show(solutions, with_fitness=True, diffs=True, notes=None):
        for i, solution in enumerate(solutions):
            label = solution.attributes.get("label", "?")
            parents = solution.attributes.get("parents") or []
            head = f"  {label:<6}"
            if parents:
                head += f" from {' + '.join(map(str, parents)):<9}"
            if with_fitness:
                head += f" fitness={solution.objectives[0]}"
            head += f"  edits={len(solution)} [{edit_names(solution)}]"
            if notes:
                head += f"  {notes[i]}"
            print(head)
            if diffs:
                for line in changes_vs_original(solution):
                    print("      " + short(line))

    state = {"generation": 0, "after_crossover": []}

    def tracer(stage, solutions):
        """Called by the Repaired GA at every stage of the pipeline."""
        if stage == "initial":
            banner("INITIAL POPULATION (the original AST + one random edit each)")
            show(solutions, with_fitness=False)
        elif stage == "evaluation":
            if state["generation"] == 0:
                print("\n--- initial population evaluated ---")
            else:
                print(f"\n--- 4. evaluation: fitness of the {len(solutions)} offspring ---")
            show(solutions, diffs=False)
        elif stage == "selection":
            state["generation"] += 1
            banner(f"GENERATION {state['generation']}")
            print("--- 1. selection: parents picked from a copy of the population ---")
            show(solutions, diffs=False)
        elif stage == "crossover":
            state["after_crossover"] = solutions
            print("\n--- 2. crossover: a subtree is exchanged between two parents "
                  "(changes vs. the original) ---")
            show(solutions, with_fitness=False)
        elif stage == "mutation":
            print("\n--- 3. mutation (repair via the operators): one swap or replacement "
                  "edit is added ---")
            notes = []
            for child, before in zip(solutions, state["after_crossover"]):
                added = [type(edit).__name__ for edit in child.edit_list[len(before.edit_list):]]
                notes.append("mutation: +" + ", ".join(added) if added
                             else "mutation: nothing applied")
            show(solutions, with_fitness=False, notes=notes)
        elif stage == "kept":
            print(f"\n--- 5a. survival: only the top {algorithm.k} of the old population "
                  f"enter the competition ---")
            show(solutions, diffs=False)
        elif stage == "survival":
            print(f"\n--- 5. survival: the best {algorithm.population_size} of "
                  f"(kept + offspring) are the new population ---")
            show(solutions, diffs=False)

    # keep only the framework's evaluation prints quiet
    _evaluate = problem.evaluate

    def _quiet_evaluate(solution):
        with quiet():
            return _evaluate(solution)

    problem.evaluate = _quiet_evaluate

    POPULATION = OFFSPRING = args.population
    K = max(1, POPULATION // 2)      # topk: survivors of the old population (K + OFFSPRING >= POPULATION)
    GA_CLASSES = {"repaired": "RepairedGeneticAlgorithm", "logging": "LoggingGeneticAlgorithm",
                  "topk": "TopKSelectorGeneticAlgorithm"}
    GeneticAlgorithmClass = _load("repairedga", GA_CLASSES[args.ga_class])
    RepairedGeneticAlgorithm = _load("repairedga", "RepairedGeneticAlgorithm")

    ga_arguments = dict(
        problem=problem, population_size=POPULATION, offspring_population_size=OFFSPRING,
        mutation=mutation, crossover=crossover, selection=BinaryTournamentSelection(),
        termination_criterion=StoppingByEvaluations(
            max_evaluations=POPULATION * (args.generations + 1)),
        trace=tracer)
    if args.ga_class == "topk":
        ga_arguments["k"] = K
    algorithm = GeneticAlgorithmClass(**ga_arguments)

    # make sure the Repaired GA is really the one in use
    assert isinstance(algorithm, RepairedGeneticAlgorithm), "not a RepairedGeneticAlgorithm"
    names = [cls.__name__ for cls in type(algorithm).__mro__]
    banner("PIPELINE")
    print("GA class           :", " -> ".join(names[:names.index("GeneticAlgorithm") + 1]))
    weights = {op: float(op.get_weight_initial()) for op in mutation.operators}
    print("mutation operators :", ", ".join(
        f"{op.__name__} ({100 * w / sum(weights.values()):.0f}%)" for op, w in weights.items()))
    print("crossover          : RustSubtreeCrossover (subtree exchange)")
    print("pair checker       :", pair_checker if pair_checker is not None else "none")
    print(f"population {POPULATION}, offspring {OFFSPRING}"
          + (f", top-k {K}" if args.ga_class == "topk" else "")
          + f", generations {args.generations}"
          + ("  [fake fitness: --dry-run]" if args.dry_run else ""))

    algorithm.run()

    best = algorithm.result() if hasattr(algorithm, "result") else algorithm.get_result()
    best = best[0] if isinstance(best, list) else best
    banner("GA BEST")
    print(f"{best.attributes.get('label', '?')}  fitness: {best.objectives[0]}")
    print(source(best))
    sys.exit(0)

# ==========================================================================
# default: one mutation and one crossover, each with its own parents
#   mutation   : mutation_parent                        -> mutant
#   crossover  : crossover_parent_1, crossover_parent_2 -> child_1, child_2
# ==========================================================================
with quiet():
    mutation_parent = problem.create_solution()
    mutant = mutation.execute(mutation_parent.clone())

    crossover_parent_1 = problem.create_solution()
    crossover_parent_2 = problem.create_solution()
    child_1, child_2 = crossover.execute([crossover_parent_1, crossover_parent_2])

banner("AST BEFORE MUTATION")
print(source(mutation_parent))

banner("AST AFTER MUTATION")
print(source(mutant))

banner("MUTATION SUMMARY")
if len(mutant) == len(mutation_parent):
    print("No mutation applied (nothing eligible, or the edit could not be applied).")
else:
    edit = mutant.edit_list[-1]
    edit_file = getattr(edit, "target_file", None) or edit._target[0]
    marked = strip_marks_tree(mutation_parent.ast[edit_file]).accept(MarkingVisitor())
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

if args.evaluate:
    banner("FITNESS")
    for label, patch in [("mutation parent", mutation_parent), ("mutant", mutant),
                         ("crossover parent 1", crossover_parent_1),
                         ("crossover parent 2", crossover_parent_2),
                         ("child 1", child_1), ("child 2", child_2)]:
        with quiet():
            problem.evaluate(patch)
        print(f"{label}: {patch.fitness}")