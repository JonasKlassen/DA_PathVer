# Dependent Assertion Path Verifier

DA_PathVer is an SMT-based tool for checking program properties over a supplied execution path. Its property language is inspired by dependent assertion logic and can refer to entry and return states, intermediate states, nested calls, and repeated procedure bodies.

Given a program, a finite control-flow trace, an execution configuration, and a property, the tool constructs symbolic constraints and searches for a counterexample. The trace fixes the sequence of control-flow events, while memory values remain symbolic wherever the program and property leave them unconstrained. A check therefore covers the encoded memory valuations compatible with that trace, rather than just the concrete values from one test run.

The current program frontend accepts Repeat-Arr, a small imperative language with integer arrays, procedure calls, and repetition. The core approach is the combination of trace-dependent memory, feasibility constraints, and assertions over selected states. The sections below describe that approach and its implemented capabilities, followed by usage instructions and input-format references.

## Theoretical Background

The approach draws on Lukas Grätz's [*Dependent Assertions for Specification and Control Flow Verification*](https://doi.org/10.26083/tuda-8042) (2026), particularly its treatment of dynamic indices and dependent assertion logic, and his manuscript *A Program Semantics with Dynamic State Indices* (2026).

### Dynamic indices and symbolic memory

A source statement can execute several times, in different calls or iterations. A **dynamic index** identifies a particular occurrence using statement numbers and nesting markers. For example, `6.1.#` identifies the return of the call at statement `1` inside the call at statement `6`. These indices let a property distinguish states that share the same source code location.

The underlying *dynx semantics* separates execution into three layers:

1. **Control flow:** the supplied trace records statement occurrences, calls, repeats, and returns.
2. **Memory:** symbolic constraints describe assignments, unchanged values, parameter passing, and the propagation of reference arguments and global variables. Unconstrained initial values represent nondeterministic choices.
3. **Feasibility:** additional constraints require conditional returns and computed call targets to agree with the chosen trace.

The implementation combines the memory and feasibility constraints into a domain formula `D`. This formula describes the encoded executions that follow the supplied control flow. The user supplies the path directly or obtains it with the trace generator. The verifier does not automatically explore alternative paths.

Memory is currently modeled with SMT arrays from integers to integers. A scalar `x` is shorthand for `x[0]`, and updating one array element preserves the others. Integers and arrays have no machine overflow or fixed size in this model. Fresh local values can remain unconstrained, allowing different executions to follow the same trace. A local named `rand`, for example, has no built-in random behavior.

### Properties over traces

A classical pre/postcondition contract relates a procedure's entry and exit. DA properties can express that contract shape and can also relate conditions at intermediate states selected by dynamic-index patterns. The same program variable can have different values at each selected state. Unlike a conventional modular contract checker, DA_PathVer requires those states to be selected explicitly within a supplied trace.

Two modal operators specify where an assertion must hold:

- `[r](A)` is a **box**: assertion `A` must hold at every position selected by `r` within the supplied trace.
- `{r}(A)` is a **diamond**: assertion `A` must hold at at least one selected position.

These modalities select positions within an execution. They do not select alternative execution paths. Nested modalities extend the current dynamic-index prefix: `[6]([1.#](A))` selects the nested return `6.1.#`. At the root, `[#](A)` refers to the outermost return.

For example, the included dice game can express a condition on a particular roll's result:

```text
[6.1.#](1 <= dice & dice <= 6)
```

It can also relate an array before and after the helper call:

```text
FORALL i : (([6](seen[i] == 1)) => ([7](seen[i] == 1)))
```

Here, `seen[i]` is read in two different memory states, while the quantified integer `i` keeps the same value across both modalities. The property requires each previously set array entry to remain set after the call. Quantifiers range over integers, independently of the finite set of trace positions.

Selectors support concatenation, union, and zero-or-more repetition. A box over an empty selection is true, and a diamond over an empty selection is false. Wildcards match one dynamic-index component, and `eps` matches the empty suffix.

### From a property to an SMT query

SMT (satisfiability modulo theories) solving checks whether logical constraints over values such as integers and arrays admit a satisfying assignment. DA_PathVer translates the property into a formula `P`, resolving boxes into conjunctions and diamonds into disjunctions over matching trace positions. Integer quantifiers remain in the SMT formula.

The solver checks:

```text
D AND NOT P
```

If this is satisfiable, the model supplies values consistent with the encoded trace that violate the property. The watch list exposes selected values from that countermodel. If it is unsatisfiable, no counterexample exists in the encoded domain for this trace.

This is a single-trace guarantee. It does not establish correctness for other paths, arbitrary iteration counts, or all inputs regardless of control flow. An infeasible trace makes `D` unsatisfiable, so the counterexample query has no model. The current CLI and GUI do not perform a separate feasibility query before reporting that no counterexample was found.

## Current Capabilities

| Area | Implemented behavior |
| --- | --- |
| Symbolic state | Integer arrays, scalar access at index `0`, array updates, and persistence of unchanged values. |
| Procedure state | Local and global variables, value arguments, reference-result propagation, and fresh non-parameter locals on calls. |
| Control flow | Encoding of supplied traces containing nested calls, repetition, conditional returns, and computed call targets. Recursive examples are included. |
| Expressions | Integer addition and subtraction, comparisons, and logical operations represented with configured integer truth values. |
| Properties | Comparisons, Boolean connectives, integer quantifiers, scalar and indexed array reads, `@fn`, and modal assertions over trace positions. |
| Solver workflow | PySMT constraints, solver selection with Z3 included as a dependency, and inspection of selected countermodel values. |
| Interfaces | CLI and Tkinter GUI for property checking, concrete trace generation, and a property editor. |

Trace generation executes a program with concrete initial parameter values and writes a trace and target mapping. Those input values are not automatically added as assumptions to subsequent symbolic verification, so any required input restriction must be expressed in the property.

### Scope and current limitations

The implementation is a prototype for finite, supplied traces. It does not provide exhaustive path exploration, induction over loops or recursion, a general termination proof, or probability calculations. Repeat-Arr is the available frontend. A Rust frontend and richer data types are not currently implemented. Extending the source language would also require corresponding symbolic semantics.

Property array indices should be integer literals or bound logical variables. General index expressions and program-variable indices are not supported by the property resolver. Solver support and performance also depend on the resulting quantified integer/array formulas.

## Implementation Overview

| Component | Responsibility |
| --- | --- |
| [`program/`](program/) | Program grammar, generated parser, and abstract syntax tree construction. |
| [`program_formula_builder.py`](execution/program_formula_builder.py) | Trace loading, symbolic memory construction, and feasibility constraints. |
| [`property/`](property/) | Property grammar, generated parser, and abstract syntax tree construction. |
| [`property_formula_builder.py`](execution/property_formula_builder.py) | Trace-selector resolution and translation of property formulas into PySMT formulas. |
| [`trace_generator.py`](execution/trace_generator.py) | Concrete execution and generation of dynamic-index traces and target mappings. |
| [`execution/`](execution/) | CLI and GUI orchestration of parsing, formula construction, solving, and result inspection. |

The [nondeterministic program example](examples/nondeterministic_program/) illustrates how a computed call target constrains values in the trace. The [dice game](examples/dice_game/) illustrates nondeterministic local values, repeated calls, reference arguments, and global state. The [Fibonacci example](examples/fibonacci/) illustrates recursive calls. All three include programs, traces, execution configurations, and properties for experimentation.

## Installation

From the directory containing the `DA_PathVer` package:

```bash
python -m venv .venv
.\.venv\Scripts\pip install -r DA_PathVer\requirements.txt
```

The project depends on PySMT, Z3, and the ANTLR Python runtime. The generated parser files are already included, so ANTLR is only needed when changing either grammar.

To regenerate the program parser after grammar changes:

```bash
cd DA_PathVer\program\antlr
java -jar C:\antlr\antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor repeat_arr.g4
```
This requires the ANTLR software (`https://www.antlr.org/download/antlr-4.13.2-complete.jar`) to be in the folder `C:\antlr`.

To regenerate the property parser after grammar changes:

```bash
cd DA_PathVer\property\antlr
java -jar C:\antlr\antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor property.g4
```

## Running

Run commands from the directory that contains the `DA_PathVer` package.

Start the GUI:

```bash
python -m DA_PathVer.execution.main
```

Run the CLI:

```bash
python -m DA_PathVer.execution.cli [COMMAND] [OPTIONS]
```

## CLI

`run` checks a property against a program, execution configuration, and trace.

```bash
python -m DA_PathVer.execution.cli run --program FOLDER --trace NUM --solver NAME --property PROPERTY_FILE_OR_NUM --watch WATCH_ITEMS
```

Example:

```bash
python -m DA_PathVer.execution.cli run --program DA_PathVer\examples\dice_game --trace 1 --solver z3 --property 1 --watch count@0
```

`generate-trace` creates a new concrete trace and updates the matching configuration file.

```bash
python -m DA_PathVer.execution.cli generate-trace --program FOLDER --input INPUTS --trace NUM --configuration SOURCE_NUM
```

Example:

```bash
python -m DA_PathVer.execution.cli generate-trace --program DA_PathVer\examples\dice_game --input count=3 --trace 4 --configuration 1
```

For all options:

```bash
python -m DA_PathVer.execution.cli [COMMAND] --help
```

## Project Folder Layout

Each verified program folder must contain:

1. `program.txt`: Repeat-Arr source code.
2. `traceN.txt`: Concrete execution trace, for example `trace1.txt`.
3. `configurationN.json`: Configuration matching the trace, including `target` and `const`.
4. `propertyN.txt`: Property file, for example `property1.txt`.

Example layout:

```text
my_program\
program.txt
trace1.txt
configuration1.json
property1.txt
```

## GUI Workflow

Step 1: Process Program and Trace

1. Select the program folder.
2. Select the trace number.
3. Select the solver, usually `z3`.
4. Click `Step 1: Process Program & Trace`.

This parses the program, loads the trace and configuration JSON, builds the symbolic domain, and populates variable and trace selection lists.

Step 2: Watch List Selection

1. Select a variable.
2. Select a trace element.
3. Optionally choose an array index or index range.
4. Click `Add to Watch`.

Watched values are displayed if the solver finds a countermodel.

Step 3: Check Property

1. Select the property number.
2. Click `Step 3: Check Property`.

If the domain together with the negated property is satisfiable, the GUI reports a counterexample. If the solver determines that the query is unsatisfiable, it reports that no counterexample was found for the selected trace, subject to the scope described above.

Optional: Generate a New Trace

1. Select the program folder.
2. Click `Create New Trace`.
3. Enter the trace number.
4. Click `Load Parameters`.
5. Enter initial values for the entry function parameters.
6. Click `Generate Trace`.

If the target `configurationN.json` does not exist, the GUI can copy an existing `configuration*.json` file from the same folder.

Optional: Create or Edit a Property

1. Click `Create/Edit Property`.
2. Select the property number.
3. Edit the formula.
4. Save it.

The saved property uses the plain grammar symbols such as `EXISTS`, `FORALL`, `{}`, `=>`, and `<=>`.

## Current Program Frontend

Repeat-Arr supplies the current input syntax for the state and control-flow features described above. This section is a practical source-format reference.

Every program starts with variable declarations followed by one or more function declarations. Each variable must be declared exactly once as either `local` or `global`.

```text
local count, seen, dice, a, b, rand
global prize

fn GAME (count)
seen[1] = FALSE
seen[2] = FALSE
seen[3] = FALSE
seen[4] = FALSE
seen[5] = FALSE
seen[6] = FALSE
call ROLL_MULT (count, ref seen)
prize = seen[6]
return

fn ROLL_MULT (count, seen)
if count <= 0 return
call ROLL_ONCE (ref dice)
seen[dice] = TRUE
count = count - 1
repeat

fn ROLL_ONCE (dice)
a = rand[0] <= 0
b = (rand[1] <= 0) + (rand[2] <= 0)
dice = 1 + a + b + b
return
```

Local variables are scoped to function activations. Global variables are visible in every function and persist across function calls. A global variable cannot be passed as a `ref` argument.

Function names can be written as constants such as `GAME` or `ROLL_MULT`. Before parsing, these constants are replaced using the `const` section of the selected `configurationN.json`.

The complete source syntax is defined in the [program grammar](program/antlr/repeat_arr.g4).

## Trace Files

A trace file is a plain text file where each line represents one execution step.

The symbolic state at a statement index is the state before that statement executes. An assignment's effect is visible at the next trace position. Return markers expose the state at the corresponding return.

Special trace elements:

- `epsilon`: Entry point before the first statement.
- `N`: Statement index in the current function, starting at 0.
- `prefix.N`: Statement index inside a nested function call or repeat.
- `#`: Function or program termination.
- `$`: Repeat block entry.

Example:

```text
epsilon
0
1
1.0
1.#
2
#
```

## Configuration JSON

`configurationN.json` maps trace positions to function IDs and defines constants.

```json
{
  "target": {
    "epsilon": 1,
    "1": 2
  },
  "const": {
    "TRUE": 1,
    "FALSE": 0,
    "MAIN": 1,
    "HELPER": 2
  }
}
```

Fields:

- `target`: Maps entry points and call trace positions to function IDs.
- `const`: Defines source-level constants that are replaced before parsing.

`TRUE` and `FALSE` should normally be provided as integer constants, usually `1` and `0`.

## Property Language

Properties describe conditions over program variables at selected trace positions.

Modal forms:

- `[trace](formula)`: Box modality. The formula must hold at every matching position in the supplied trace.
- `{trace}(formula)`: Diamond modality. The formula must hold at some matching position in the supplied trace.

Quantifiers:

- `EXISTS i : (formula)`
- `FORALL i : (formula)`

Program variables can be read as scalars or arrays:

```text
count
seen[6]
seen[i]
@fn
```

Example property:

```text
[#](FORALL i : (FORALL j : ((1 <= i & j <= 6 & i < j) => seen[i] <= seen[j])))
```

Selectors can combine dynamic-index components with concatenation (`r.s`), union (`(r U s)`), and repetition (`(r)*`). The complete syntax is defined in the [property grammar](property/antlr/property.g4).
