# Repeat-Arr Verifier

Repeat-Arr Verifier is a standalone symbolic execution and contract verification tool for programs written in the Repeat-Arr language. It includes a command-line interface, a Tkinter GUI, parsers and examples.

## Installation

From the repository root:

```bash
python -m venv .venv
.\.venv\Scripts\pip install -r repeat_arr_verifier\requirements.txt
```

The project depends on PySMT, Z3, and the ANTLR Python runtime. The generated parser files are already included, so ANTLR is only needed when changing `program/antlr/repeat_arr.g4` or `contract/antlr/contract.g4`.

To regenerate the program parser after grammar changes:

```bash
cd repeat_arr_verifier\program\antlr
java -jar C:\antlr\antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor repeat_arr.g4
```
This requires the ANTLR software (`https://www.antlr.org/download/antlr-4.13.2-complete.jar`) to be in the folder `C:\antlr`.

## Running

Run commands from the directory that contains the `repeat_arr_verifier` package.

Start the GUI:

```bash
python -m repeat_arr_verifier.execution.main
```

Run the CLI:

```bash
python -m repeat_arr_verifier.execution.cli [COMMAND] [OPTIONS]
```

## CLI

`run` verifies a contract against a program, execution config, and trace.

```bash
python -m repeat_arr_verifier.execution.cli run --program FOLDER --trace NUM --solver NAME --formula CONTRACT_FILE_OR_NUM --watch WATCH_ITEMS
```

Example:

```bash
python -m repeat_arr_verifier.execution.cli run --program repeat_arr_verifier\examples\dice_game --trace 1 --solver z3 --formula 1 --watch count@0
```

`generate-trace` creates a new concrete trace and updates the matching execution file.

```bash
python -m repeat_arr_verifier.execution.cli generate-trace --program FOLDER --input INPUTS --trace NUM --execution SOURCE_NUM
```

Example:

```bash
python -m repeat_arr_verifier.execution.cli generate-trace --program repeat_arr_verifier\examples\dice_game --input count=3 --trace 4 --execution 1
```

For all options:

```bash
python -m repeat_arr_verifier.execution.cli [COMMAND] --help
```

## Project Folder Layout

Each verified program folder must contain:

1. `program.txt`: Repeat-Arr source code.
2. `traceN.txt`: Concrete execution trace, for example `trace1.txt`.
3. `executionN.json`: Configuration matching the trace, including `target` and `const`.
4. `contractN.txt`: Contract file, for example `contract1.txt`.

Example layout:

```text
my_program\
program.txt
trace1.txt
execution1.json
contract1.txt
```

## GUI Workflow

Step 1: Process Program and Trace

1. Select the program folder.
2. Select the trace number.
3. Select the solver, usually `z3`.
4. Click `Step 1: Process Program & Trace`.

This parses the program, loads the trace and execution JSON, builds the symbolic domain, and populates variable and trace selection lists.

Step 2: Watch List Selection

1. Select a variable.
2. Select a trace element.
3. Optionally choose an array index or index range.
4. Click `Add to Watch`.

Watched values are displayed if the solver finds a countermodel.

Step 3: Solve Contract

1. Select the contract number.
2. Click `Step 3: Solve Contract`.

If the negated contract is satisfiable, the GUI reports a countermodel. Otherwise, it reports that the contract is valid for the selected trace.

Optional: Generate a New Trace

1. Select the program folder.
2. Click `Create New Trace`.
3. Enter the trace number.
4. Click `Load Parameters`.
5. Enter initial values for the entry function parameters.
6. Click `Generate Trace`.

If the target `executionN.json` does not exist, the GUI can copy an existing `execution*.json` file from the same folder.

Optional: Create or Edit a Contract

1. Click `Create/Edit Contract`.
2. Select the contract number.
3. Edit the formula.
4. Save it.

The saved contract uses the plain grammar symbols such as `EXISTS`, `FORALL`, `{}`, `=>`, and `<=>`.

## Program Language

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

Function names can be written as constants such as `GAME` or `ROLL_MULT`; constants are replaced using the `const` section of the selected `executionN.json` before parsing.

### Program Grammar

```antlr
grammar repeat_arr;

program: varDecl+ functionDecl+ EOF;

varDecl: 'local' varList | 'global' varList;

functionDecl: 'fn' INTEGER '(' paramList? ')' stmt+;

paramList: varList;

varList: var (',' var)*;

stmt: call | assign | ret | 'repeat';

call: 'call' expr '(' argList? ')';

argList: arg (',' arg)*;

arg: 'ref' var | var;

assign: var ('[' expr ']')? '=' expr;

ret: ('if' expr)? 'return';

expr: expr ('=='|'<='|'<'|'!='|'>='|'>') expr
    | expr ('&'|'|') expr
    | expr ('+'|'-') expr
    | expr ('=>'|'<=>') expr
    | atom;

atom: INTEGER
    | 'TRUE'
    | 'FALSE'
    | var
    | var '[' expr ']'
    | '(' expr ')';

var: ID | '@fn';

INTEGER: '-'?[0-9]+;
ID: [a-z]+;
```

## Trace Files

A trace file is a plain text file where each line represents one execution step.

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

## Execution JSON

`executionN.json` maps trace positions to function IDs and defines constants.

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

## Contract Language

Contracts describe properties over trace positions and program variables.

Modal forms:

- `[trace](formula)`: Box modality. The formula must hold at every matching trace.
- `{trace}(formula)`: Diamond modality. The formula must hold at some matching trace.

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

Example contract:

```text
[#](FORALL i : (FORALL j : ((1 <= i & j <= 6 & i < j) => seen[i] <= seen[j])))
```

### Contract Grammar

```antlr
contract
    : '(' contract ')'
    | ('EXISTS'|'FORALL') VAR ':' '(' contract ')'
    | contract ('=='|'<='|'<'|'!='|'>='|'>') contract
    | '!' contract
    | contract ('&'|'|') contract
    | contract ('=>'|'<=>') contract
    | '[' trace ']' '(' contract ')'
    | '{' trace '}' '(' contract ')'
    | contract_atom;

trace
    : '(' trace ')' '*'
    | '(' trace 'U' trace ')'
    | trace '.' trace
    | trace_atom;

contract_atom: VAR | indexed_var | '@fn' | INT;

indexed_var: VAR '[' (INT|VAR) ']';

trace_atom: '?' | '$' | '#' | INT | 'eps';
```
