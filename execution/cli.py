import argparse
import json
import os
import sys
# Add project root to sys.path so we can import repeat_arr_verifier packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import *
from pysmt.shortcuts import Solver, Not, get_env, Select, Int

# These imports assume we are in the project root
from repeat_arr_verifier.contract.antlr.contractLexer import contractLexer
from repeat_arr_verifier.contract.antlr.contractParser import contractParser
from repeat_arr_verifier.contract.ast.contract_ast_builder import ContractASTBuilder
from repeat_arr_verifier.execution.contract_formula_builder import ContractFormulaBuilder
from repeat_arr_verifier.execution.program_formula_builder import ProgramFormulaBuilder, load_trace
from repeat_arr_verifier.program.antlr.repeat_arrLexer import repeat_arrLexer
from repeat_arr_verifier.program.antlr.repeat_arrParser import repeat_arrParser
from repeat_arr_verifier.program.ast.program_ast_builder import ProgramASTBuilder
from repeat_arr_verifier.execution.trace_generator import TraceGenerator

def run_solver(args):
    folder = args.program
    trace_num = args.trace
    contract_file = args.formula
    solver_name = args.solver
    watch_items_str = args.watch

    program_path = os.path.join(folder, "program.txt")
    trace_path = os.path.join(folder, f"trace{trace_num}.txt")
    execution_path = os.path.join(folder, f"execution{trace_num}.json")
    
    if not os.path.exists(program_path) or not os.path.exists(trace_path) or not os.path.exists(execution_path):
        print("Error: Missing program, trace, or execution file.")
        sys.exit(1)

    # 1. Process Program
    with open(execution_path, 'r') as f:
        execution = json.load(f)

    with open(program_path) as f:
        program_content = f.read()
        for const_name, const_value in execution.get('const', {}).items():
            program_content = program_content.replace(const_name, str(const_value))
        input_stream = InputStream(program_content)

    lexer = repeat_arrLexer(input_stream)
    parser = repeat_arrParser(CommonTokenStream(lexer))
    ast = ProgramASTBuilder().visit(parser.program())

    executor = ProgramFormulaBuilder(ast, execution)
    trace_info = load_trace(ast, trace_path, execution['target'])
    domain = executor.build_domain(trace_info)

    # 2. Process Contract
    if not os.path.exists(contract_file):
        # Try constructing path if it's a number
        possible_path = os.path.join(folder, f"contract{contract_file}.txt")
        if os.path.exists(possible_path):
            contract_file = possible_path
        else:
            print(f"Error: Contract file not found: {contract_file}")
            sys.exit(1)

    with open(contract_file) as f:
        contract_content = f.read()
        for const_name, const_value in execution.get('const', {}).items():
            contract_content = contract_content.replace(const_name, str(const_value))
        contract_input_stream = InputStream(contract_content)

    contract_lexer = contractLexer(contract_input_stream)
    contract_parser = contractParser(CommonTokenStream(contract_lexer))
    contract_ast = ContractASTBuilder().visit(contract_parser.contract())

    cfb = ContractFormulaBuilder(trace_info, executor.idx_vars)
    problem = cfb.resolve_formula(contract_ast)

    if problem is None:
        print("Contract found no matching cases.")
        return

    # 3. Solve
    with Solver(name=solver_name) as solver:
        solver.add_assertion(domain)
        solver.add_assertion(Not(problem))
        
        if solver.solve():
            print("RESULT: Counter model found (Contract is NOT valid)")
            if watch_items_str:
                model = solver.get_model()
                # Parse watch items
                # Example: i[2]@#,count,res@#
                # I need to know how to map this to the format var[idx] @ trace
                # The user's example is ambiguous. I will assume they want 
                # a list of "var[idx]@trace" format.
                # If they pass "i[2]@#,count,res@#", maybe they mean:
                # "i[2]@#", "count", "res@#" ... this is hard.
                # I'll implement a simple split for now and hope it matches.
                watch_items = watch_items_str.split(',')
                for item in watch_items:
                    # Basic parser for item
                    # Assuming format: var[idx]@trace
                    # Or maybe trace is optional?
                    parts = item.split('@')
                    var_idx = parts[0] # i[2]
                    trace = parts[1] if len(parts) > 1 else "epsilon" # # 

                    import re
                    match = re.match(r"(.+?)(?:\[(\d+)\])?$", var_idx)
                    if match:
                        var, idx_val = match.groups()
                        idx_val = int(idx_val) if idx_val else 0
                        if var in executor.idx_vars and trace in executor.idx_vars[var]:
                            sym = executor.idx_vars[var][trace][0]
                            val = model.get_value(Select(sym, Int(idx_val)))
                            print(f"{var}[{idx_val}] @ {trace}: {val}")
                        else:
                            print(f"{var}[{idx_val}] @ {trace}: NOT FOUND")
                    else:
                        print(f"Could not parse watch item: {item}")
        else:
            print("RESULT: Contract is valid")

def generate_trace(args):
    folder = args.program
    input_values = ' '.join(args.input) if isinstance(args.input, list) else args.input
    # How to interpret "VALUES"? The user said "--input VALUES"
    # In gui.py: initial_values[param] = {index: value}
    
    # I'll assume VALUES is a path to a JSON file or a stringified JSON
    try:
        if os.path.exists(input_values):
            with open(input_values, 'r') as f:
                initial_values = json.load(f)
        else:
            initial_values = json.loads(input_values)
        
        # Convert keys in initial_values to integers if possible
        for var, val in initial_values.items():
            if isinstance(val, dict):
                initial_values[var] = {int(k): v for k, v in val.items()}
                
    except Exception as e:
        # Try to parse as key=value, key=value
        try:
            import re
            initial_values = {}
            parts = re.split(r'[, ]+', input_values)
            for part in parts:
                if not part: continue
                if '=' in part:
                    k, v = part.split('=')
                    initial_values[k.strip()] = {'0': int(v.strip())}
        except Exception as inner_e:
            print(f"Error parsing input values: {inner_e}")
            sys.exit(1)

    # I need to know the trace number to generate.
    # The example is `python generate-trace --program FOLDER --input VALUES`
    # I have --trace and optional --execution.
    trace_num = args.trace
    execution_num = args.execution if args.execution else trace_num
    
    # Use TraceGenerator
    try:
        execution_path_src = os.path.join(folder, f"execution{execution_num}.json")
        execution_path_dst = os.path.join(folder, f"execution{trace_num}.json")
        program_path = os.path.join(folder, "program.txt")
        trace_out_path = os.path.join(folder, f"trace{trace_num}.txt")

        with open(execution_path_src, 'r') as f:
            execution_config = json.load(f)

        with open(program_path) as f:
            program_content = f.read()
            for const_name, const_value in execution_config.get('const', {}).items():
                program_content = program_content.replace(const_name, str(const_value))

        input_stream = InputStream(program_content)
        lexer = repeat_arrLexer(input_stream)
        parser = repeat_arrParser(CommonTokenStream(lexer))
        ast = ProgramASTBuilder().visit(parser.program())

        start_func_id = execution_config.get('target', {}).get('epsilon')
        if start_func_id is None:
            if 'GAME' in execution_config.get('const', {}):
                start_func_id = execution_config['const']['GAME']
            else:
                raise ValueError("'epsilon' not found in target map and no 'GAME' constant.")
        
        generator = TraceGenerator(ast, execution_config, initial_values)
        
        # Ensure we start with a clean target map for new generation
        generator.target = {}
        if "epsilon" not in generator.target:
            generator.target["epsilon"] = start_func_id
        
        if start_func_id in ast.functions:
            func = ast.functions[start_func_id]
        else:
            for k, v in execution_config.get('const', {}).items():
                if v == start_func_id and k in ast.functions:
                    func = ast.functions[k]
                    break
                if k == start_func_id and v in ast.functions:
                    func = ast.functions[v]
                    break
        
        if not func:
            raise ValueError(f"Function {start_func_id} not found.")

        args_list = []
        for param in func.params:
            # initial_values[param] is a dict {index: value}
            val = initial_values.get(param, {0: 0})
            if len(val) == 1 and 0 in val:
                args_list.append(val[0])
            else:
                args_list.append(val)

        # Find human-readable name if possible
        func_name = str(start_func_id)
        for name, value in execution_config.get('const', {}).items():
            if value == start_func_id:
                func_name = name
                break
        
        print(f"Generating trace for {func_name} ({start_func_id})...")
        trace, updated_target = generator.generate(start_func_id, args_list)

        # Save trace
        with open(trace_out_path, 'w') as f:
            f.write("\n".join(trace))
        
        # Update execution.json
        execution_config['target'] = updated_target
        with open(execution_path_dst, 'w') as f:
            json.dump(execution_config, f, indent=2)

        print(f"Successfully generated {trace_out_path} and updated {execution_path_dst}")

    except Exception as e:
        print(f"Error generating trace: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Symbolic Execution CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run symbolic execution and verify contracts")
    run_parser.add_argument("--program", required=True, help="Path to the program folder (must contain program.txt, executionN.json, traceN.txt)")
    run_parser.add_argument("--trace", required=True, help="Trace number (N) to use (e.g., 1)")
    run_parser.add_argument("--solver", required=True, help="Name of the solver to use (e.g., z3)")
    run_parser.add_argument("--formula", required=True, help="Path to contract file or contract number (e.g., 1 for contract1.txt)")
    run_parser.add_argument("--watch", help="Comma-separated list of watch items (format: var[idx]@trace, e.g., count[0]@#,res@#)")

    # Generate Trace command
    gen_parser = subparsers.add_parser("generate-trace", help="Generate a new symbolic execution trace")
    gen_parser.add_argument("--program", required=True, help="Path to the program folder")
    gen_parser.add_argument("--input", required=True, nargs='+', help="Input values (format: param1=val1, param2=val2, or JSON string)")
    gen_parser.add_argument("--trace", required=True, help="New trace number (N) to create (e.g., 2)")
    gen_parser.add_argument("--execution", help="Optional execution number to use as a source configuration (defaults to trace number if not provided)")

    args = parser.parse_args()

    if args.command == "run":
        run_solver(args)
    elif args.command == "generate-trace":
        generate_trace(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
