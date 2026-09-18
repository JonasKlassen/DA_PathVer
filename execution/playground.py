import json
import os
from antlr4 import *
from DA_PathVer.program.antlr.repeat_arrLexer import repeat_arrLexer
from DA_PathVer.program.antlr.repeat_arrParser import repeat_arrParser
from DA_PathVer.program.ast.program_ast_builder import ProgramASTBuilder
from DA_PathVer.execution.trace_generator import TraceGenerator

def run_playground():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    example_dir = os.path.join(base_dir, "examples", "dice_game")
    program_path = os.path.join(example_dir, "program.txt")
    execution_path = os.path.join(example_dir, "execution2.json")

    print(f"Loading program from: {program_path}")
    
    # 1. Load and parse the program
    with open(execution_path, 'r') as f:
        execution_config = json.load(f)

    with open(program_path, 'r') as f:
        program_content = f.read()
        # Apply constants to the program source if necessary (as in gui.py)
        for const_name, const_value in execution_config.get('const', {}).items():
            program_content = program_content.replace(const_name, str(const_value))
    
    input_stream = InputStream(program_content)
    lexer = repeat_arrLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = repeat_arrParser(stream)
    tree = parser.program()
    
    builder = ProgramASTBuilder()
    ast = builder.visit(tree)

    # 2. Define initial values for the execution
    # For dice_game, we need count (number of rolls) and some rand values
    # rand is used in ROLL_ONCE to determine the dice value
    initial_values = {
        "count": 2,
        "prize": 0,
        # "rand": {0: 1, 1: 0, 2: 1}
    }

    print("Initial values:", initial_values)

    # 3. Instantiate TraceGenerator and generate trace
    generator = TraceGenerator(ast, execution_config, initial_values)
    
    # The 'GAME' function is the entry point, which is constant 8
    start_func = execution_config['const']['GAME']
    args = [initial_values["count"], 0] # count, prize (initial prize is 0)

    print(f"Generating trace for function {start_func}...")
    trace, target = generator.generate(start_func, args)

    # 4. Output results
    print("\n--- Generated Trace ---")
    for step in trace:
        print(step)

    print("\n--- Updated Target Map ---")
    print(json.dumps(target, indent=2))

run_playground()
