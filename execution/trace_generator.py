import json
import os
import random
import sys

from antlr4 import *

class TraceGenerator:
    def __init__(self, program, execution, initial_values):
        self.program = program
        self.execution = execution  # This is the dict from execution.json
        self.initial_values = initial_values  # dict: var_name -> initial_value (can be int or dict for arrays)
        self.trace = []
        self.target = execution.get('target', {}).copy()
        self.constants = execution.get('const', {}).copy()
        self.global_vars = set(program.global_vars)
        self.state = {} # Global state: var_name -> {index: value}

    def _evaluate(self, expr, local_state):
        from repeat_arr_verifier.program.ast.program_ast_nodes import AstInt, AstBool, Var, ArrayAccess, BinOp
        
        if isinstance(expr, AstInt):
            return expr.value
        if isinstance(expr, AstBool):
            return expr.value
        if isinstance(expr, Var):
            name = expr.name
            if name in self.global_vars:
                return self.state.get(name, {}).get(0, 0)
            if name in local_state:
                return local_state[name].get(0, 0)
            return random.randint(-sys.maxsize+1, sys.maxsize-1)
        if isinstance(expr, ArrayAccess):
            name = expr.name
            idx = self._evaluate(expr.index, local_state)
            if name in self.global_vars:
                return self.state.get(name, {}).get(idx, 0)
            if name in local_state:
                return local_state.get(name, {}).get(idx, 0)
            return random.randint(-sys.maxsize+1, sys.maxsize-1)
        if isinstance(expr, BinOp):
            left = self._evaluate(expr.left, local_state)
            right = self._evaluate(expr.right, local_state)
            if expr.op == '+':
                return left + right
            if expr.op == '-':
                return left - right
            if expr.op == '<=':
                return 1 if left <= right else 0
        return 0

    def generate(self, start_func_name, args):
        # Initialize state with initial_values
        for var, val in self.initial_values.items():
            if isinstance(val, dict):
                self.state[var] = {int(k): v for k, v in val.items()}
            else:
                self.state[var] = {0: val}
        
        # Start execution
        self.trace.append("epsilon")
        # Ensure epsilon is in target if not present
        if "epsilon" not in self.target:
            self.target["epsilon"] = start_func_name

        self._execute_function(start_func_name, args, "epsilon")
        if self.trace[-1] != "#":
            self.trace.append("#")
        
        return self.trace, self.target

    def _execute_function(self, func_name, args, prefix):
        from repeat_arr_verifier.program.ast.program_ast_nodes import Assign, Call, Return, Repeat, Var, ArrayAccess, RefArg, Arg
        
        if func_name not in self.program.functions:
            # Maybe it's a constant?
            actual_func_name = None
            for k, v in self.constants.items():
                if v == func_name:
                    actual_func_name = k
                    break
            if actual_func_name and actual_func_name in self.program.functions:
                func_name = actual_func_name
            else:
                raise ValueError(f"Function {func_name} not found in program.")

        func = self.program.functions[func_name]
        local_state = {}
        
        # Map args to params
        for param, arg_val in zip(func.params, args):
            # args are passed as values (dicts for arrays/refs)
            if isinstance(arg_val, dict):
                # Ensure keys are integers
                local_state[param] = {int(k): v for k, v in arg_val.items()}
            else:
                local_state[param] = {0: arg_val}

        i = 0
        while i < len(func.body):
            stmt = func.body[i]
            t_idx = f"{prefix}.{i}" if prefix != "epsilon" else str(i)
            self.trace.append(t_idx)
            
            if isinstance(stmt, Assign):
                val = self._evaluate(stmt.value, local_state)
                target = stmt.target
                if isinstance(target, Var):
                    if target.name in self.global_vars:
                        if target.name not in self.state: self.state[target.name] = {}
                        self.state[target.name][0] = val
                    else:
                        if target.name not in local_state: local_state[target.name] = {}
                        local_state[target.name][0] = val
                elif isinstance(target, ArrayAccess):
                    idx = self._evaluate(target.index, local_state)
                    if target.name in self.global_vars:
                        if target.name not in self.state: self.state[target.name] = {}
                        self.state[target.name][idx] = val
                    else:
                        if target.name not in local_state: local_state[target.name] = {}
                        local_state[target.name][idx] = val
                i += 1
            
            elif isinstance(stmt, Call):
                callee_func_id = self._evaluate(stmt.expr, local_state)
                self.target[t_idx] = callee_func_id
                
                # Prepare args
                call_args = []
                non_ref_args = {}
                for arg in stmt.args:
                    arg_name = arg.name
                    if isinstance(arg, RefArg) and arg_name in self.global_vars:
                        raise ValueError(f"Global variable '{arg_name}' cannot be passed as a ref argument.")
                    # Get current value of arg
                    if arg_name in self.global_vars:
                        if arg_name not in self.state: self.state[arg_name] = {}
                        val = self.state[arg_name]
                    elif arg_name in local_state:
                        val = local_state[arg_name]
                    else:
                        local_state[arg_name] = {}
                        val = local_state[arg_name]
                    
                    if isinstance(arg, RefArg):
                        call_args.append(val)
                    else:
                        call_args.append(val.copy() if isinstance(val, dict) else val)
                    if not isinstance(arg, RefArg) and arg_name not in self.global_vars:
                        # Use a deep-ish copy for dictionaries (arrays/ref types)
                        non_ref_args[arg_name] = val.copy() if isinstance(val, dict) else val

                self._execute_function(callee_func_id, call_args, t_idx)
                
                for arg_name, saved_val in non_ref_args.items():
                    if arg_name in self.global_vars:
                        self.state[arg_name] = saved_val
                    elif arg_name in local_state:
                        local_state[arg_name] = saved_val
                i += 1
            
            elif isinstance(stmt, Return):
                ret_val = self._evaluate(stmt.expr, local_state)
                if ret_val == 1: # TRUE
                    # Terminate function
                    self.trace.append(f"{prefix}.#" if prefix != "epsilon" else "#")
                    return
                i += 1
            
            elif isinstance(stmt, Repeat):
                repeat_prefix = f"{prefix}.$"
                self.trace.append(repeat_prefix)
                
                # Construct updated args from local_state
                new_args = []
                for param in func.params:
                    val = local_state[param]
                    # Convert {0: val} back to val if it was a scalar
                    if len(val) == 1 and 0 in val:
                        new_args.append(val[0])
                    else:
                        new_args.append(val)
                        
                self._execute_function(func_name, new_args, repeat_prefix)
                self.trace.append(f"{prefix}.#" if prefix != "epsilon" else "#")
                return
            
            else:
                i += 1
        
        self.trace.append(f"{prefix}.#" if prefix != "epsilon" else "#")
