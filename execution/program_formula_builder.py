import re

from pysmt.shortcuts import Symbol, Equals, And, Int, Select, Store, Plus, Minus, LE, GT, Implies, Iff, NotEquals, GE, \
    LT, Or
from pysmt.typing import ARRAY_INT_INT, INT

from DA_PathVer.program.ast.program_ast_nodes import *


def get_statement(ast, func_name, index_str, target):
    if index_str.endswith("#"):
        if not re.search(r'(?:\$\.)+#$', index_str):
            return None, func_name, True
        return None, func_name, False
    if index_str == "epsilon": return None, target['epsilon'], False
    last_part = index_str.split('.')[-1]
    func = ast.functions[func_name]
    idx = -1 if last_part == "$" else int(last_part)
    statement = func.body[idx]
    if isinstance(statement, Call): func_name = target[index_str]
    return statement, func_name, False


def load_trace(ast, path, target):
    info = []
    function_calls = [None]
    with open(path) as f:
        for line in f:
            if not line.strip(): continue
            idx_str = line.strip()
            statement, next_func, end_of_func = get_statement(ast, function_calls[-1], idx_str, target)
            info.append((idx_str, function_calls[-1], statement))
            if end_of_func:
                function_calls = function_calls[:-1]
            elif next_func != function_calls[-1]:
                function_calls.append(next_func)
    return info


class ProgramFormulaBuilder:
    def __init__(self, ast, execution):
        self.ast = ast
        self.local_vars = set(ast.local_vars)
        self.global_vars = set(ast.global_vars)
        self.func_vars = {
            f_name: self._get_vars_in_func(f) & self.local_vars
            for f_name, f in ast.functions.items()
        }
        self.variables = sorted(self.local_vars | self.global_vars)
        self.idx_vars = {} # var -> t_idx -> [curr_sym, prev_sym]
        self.inequalities = []
        self.conditions = []
        self.equalities = []
        self.TRUE = Int(execution['const']['TRUE'])
        self.FALSE = Int(execution['const']['FALSE'])
        self.call_conditions = []


    def _get_vars_in_func(self, func):
        vars_found = set()
        def walk(n):
            if isinstance(n, (Var, RefArg, Arg)):
                vars_found.add(n.name)
            elif isinstance(n, ArrayAccess): 
                vars_found.add(n.name)
                walk(n.index)
            elif isinstance(n, Assign): 
                walk(n.target)
                walk(n.value)
            elif isinstance(n, Call): 
                for a in n.args: walk(a)
            elif isinstance(n, Return): 
                walk(n.expr)
            elif isinstance(n, BinOp): 
                walk(n.left)
                walk(n.right)
            elif isinstance(n, Function):
                vars_found.update(n.params)
                for s in n.body: walk(s)
        walk(func)
        return vars_found

    def _evaluate_expr(self, node, t_idx):
        if isinstance(node, AstInt): 
            return Int(node.value)
        if isinstance(node, Var): 
            return Select(self.idx_vars[node.name][t_idx][0], Int(0))
        if isinstance(node, ArrayAccess):
            return Select(self.idx_vars[node.name][t_idx][0], self._evaluate_expr(node.index, t_idx))
        if isinstance(node, BinOp):
            left = self._evaluate_expr(node.left, t_idx)
            right = self._evaluate_expr(node.right, t_idx)
            if node.op == "+": 
                return Plus(left, right)
            if node.op == "-": 
                return Minus(left, right)
            if node.op == "<=":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(LE(left, right), Equals(res, self.TRUE)),
                    Iff(GT(left, right), Equals(res, self.FALSE))
                ))
                return res
            if node.op == "==":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(Equals(left, right), Equals(res, self.TRUE)),
                    Iff(NotEquals(left, right), Equals(res, self.FALSE))
                ))
                return res
            if node.op == ">=":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(GE(left, right), Equals(res, self.TRUE)),
                    Iff(LT(left, right), Equals(res, self.FALSE))
                ))
                return res
            if node.op == "<":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(LT(left, right), Equals(res, self.TRUE)),
                    Iff(GE(left, right), Equals(res, self.FALSE))
                ))
                return res
            if node.op == "!=":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(NotEquals(left, right), Equals(res, self.TRUE)),
                    Iff(Equals(left, right), Equals(res, self.FALSE))
                ))
                return res
            if node.op == ">":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(GT(left, right), Equals(res, self.TRUE)),
                    Iff(LE(left, right), Equals(res, self.FALSE))
                ))
                return res
            if node.op == "&":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(And(NotEquals(left, self.FALSE), NotEquals(right, self.FALSE)), Equals(res, self.TRUE)),
                    Iff(Or(Equals(left, self.FALSE), Equals(right, self.FALSE)), Equals(res, self.FALSE))
                ))
                return res
            if node.op == "|":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(Or(NotEquals(left, self.FALSE), NotEquals(right, self.FALSE)), Equals(res, self.TRUE)),
                    Iff(And(Equals(left, self.FALSE), Equals(right, self.FALSE)), Equals(res, self.FALSE))
                ))
                return res
            if node.op == "=>":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(Or(Equals(left, self.FALSE), NotEquals(right, self.FALSE)), Equals(res, self.TRUE)),
                    Iff(And(NotEquals(left, self.FALSE), Equals(right, self.FALSE)), Equals(res, self.FALSE))
                ))
                return res
            if node.op == "<=>":
                res = Symbol(f"ineq_{len(self.inequalities)}", INT)
                self.inequalities.append(And(
                    Iff(Or(And(Equals(left, self.FALSE), Equals(right, self.FALSE)), And(NotEquals(left, self.FALSE), NotEquals(right, self.FALSE))), Equals(res, self.TRUE)),
                    Iff(Or(And(Equals(left, self.FALSE), NotEquals(right, self.FALSE)), And(NotEquals(left, self.FALSE), Equals(right, self.FALSE))), Equals(res, self.FALSE))
                ))
                return res
        if isinstance(node, AstBool):
            return False
        return None

    def build_domain(self, trace_info):
        trace = [ti[0] for ti in trace_info]
        # 1. Initialize symbols. By default, they chain to the previous trace step.
        for v in self.variables:
            self.idx_vars[v] = {}
            for i, t in enumerate(trace):
                #name = f"{v}@{t}"
                name = f"{v}@{t}".replace(".","_").replace("$","dol").replace("#","hash")
                curr = Symbol(name, ARRAY_INT_INT)
                prev = self.idx_vars[v][trace[i-1]][0] if i > 0 else curr
                self.idx_vars[v][t] = [curr, prev]

        # 1.5 Initialize @fn
        v = '@fn'
        self.idx_vars[v] = {}
        for i, t in enumerate(trace):
            name = f"{v}_{t}".replace(".","_").replace("$","dol").replace("#","hash")
            curr = Symbol(name, INT)
            prev = self.idx_vars[v][trace[i - 1]][0] if i > 0 else curr
            self.idx_vars[v][t] = [curr, prev]

        # 2. Process trace to handle logic (assignments, calls, persistence)
        for i, (t_idx, f_name, stmt) in enumerate(trace_info):
            self.equalities.append(Equals(self.idx_vars['@fn'][t_idx][0], Int(f_name) if f_name else self.idx_vars['@fn'][t_idx][0]))
            if stmt:
                # Assignments update the state in the next trace step
                if isinstance(stmt, Assign) and i + 1 < len(trace_info):
                    val = self._evaluate_expr(stmt.value, t_idx)
                    next_t = trace_info[i+1][0]
                    # Update the NEXT step's predecessor state directly
                    target = stmt.target
                    if isinstance(target, Var):
                        self.idx_vars[target.name][next_t][1] = Store(self.idx_vars[target.name][next_t][1], Int(0), val)
                    elif isinstance(target, ArrayAccess):
                        idx = self._evaluate_expr(target.index, t_idx)
                        self.idx_vars[target.name][next_t][1] = Store(self.idx_vars[target.name][next_t][1], idx, val)
                    # Force equality if it was modified
                    self.equalities.append(Equals(self.idx_vars[target.name][next_t][0], self.idx_vars[target.name][next_t][1]))

                # Handle function calls: parameter passing and return persistence
                elif isinstance(stmt, Call) and i + 1 < len(trace_info):
                    next_t, callee_name, _ = trace_info[i+1]
                    callee = self.ast.functions[callee_name]

                    self.call_conditions.append(Equals(self._evaluate_expr(stmt.expr, t_idx), Int(callee_name)))

                    # Find callee exit
                    if len(t_idx) == 1:
                        after_call_t_ = str(int(t_idx) + 1)
                    else:
                        after_call_t_ = t_idx.rsplit(".", 1)
                        after_call_t_ = after_call_t_[0]+ "." + str(int(after_call_t_[1])+1)

                    callee_exit_t_ = trace[trace.index(after_call_t_)-1]

                    for v in self.global_vars:
                        self.equalities.append(Equals(self.idx_vars[v][next_t][0], self.idx_vars[v][t_idx][0]))
                        self.equalities.append(Equals(self.idx_vars[v][after_call_t_][0], self.idx_vars[v][callee_exit_t_][0]))

                    # Pass parameters to the callee
                    ref_args = []
                    for param, arg in zip(callee.params, stmt.args):
                        if isinstance(arg, RefArg):
                            if arg.name in self.global_vars:
                                raise ValueError(f"Global variable '{arg.name}' cannot be passed as a ref argument.")
                            # Backprop ref args
                            self.equalities.append(
                                Equals(self.idx_vars[arg.name][after_call_t_][0], self.idx_vars[param][callee_exit_t_][0]))
                            ref_args.append(arg.name)
                        self.equalities.append(Equals(self.idx_vars[param][next_t][0], self.idx_vars[arg.name][t_idx][0]))

                    # Callee's local variables (non-params) should start fresh
                    for v in self.func_vars[callee_name]:
                        if v not in callee.params:
                            # Link explicitly to self to ensure it's independent
                            self.equalities.append(Equals(self.idx_vars[v][next_t][0], self.idx_vars[v][next_t][0]))

                    # Other caller variables persist from the call site
                    for v in self.func_vars[f_name]:
                        if v not in ref_args:
                            self.equalities.append(
                                Equals(self.idx_vars[v][after_call_t_][0], self.idx_vars[v][t_idx][0]))


                # Conditional returns determine the next branch in the trace
                elif isinstance(stmt, Return):
                    cond = self._evaluate_expr(stmt.expr, t_idx)
                    if not cond: continue
                    is_terminal = trace[i+1].endswith("#")
                    self.conditions.append(Equals(cond, self.TRUE if is_terminal else self.FALSE))

        # 3. Finalize frame stability: link current state to the resolved predecessor
        last_entry = ['epsilon']
        for i, (t_idx, f_name, _) in enumerate(trace_info):
            if t_idx.endswith('0') and not re.search(r'(?:\$\.)+0$', t_idx):
                last_entry.append(t_idx)
            for v in self.variables:
                # Link if variable is in scope OR if we want it to chain through calls
                # Previously it only chained if in scope.
                # Check if this state was already explicitly linked
                is_linked = False
                for eq in self.equalities:
                    if eq.args()[0] == self.idx_vars[v][t_idx][0]:
                        is_linked = True
                        break
                if not is_linked:
                    if v in self.global_vars:
                        prev = self.idx_vars[v][trace[i - 1]][0] if i > 0 else self.idx_vars[v][t_idx][0]
                        self.equalities.append(Equals(self.idx_vars[v][t_idx][0], prev))
                    # ONLY chain local variables if they belong to the current function's scope
                    elif f_name is not None and v in self.func_vars[f_name] and (t_idx != '0' or v in self.ast.functions[f_name].params):
                        self.equalities.append(Equals(self.idx_vars[v][t_idx][0], self.idx_vars[v][trace[i-1]][0]))
                    else:
                        # Otherwise it remains independent (self-loop)
                        self.equalities.append(Equals(self.idx_vars[v][t_idx][0], self.idx_vars[v][last_entry[-1]][0]))

            if t_idx.endswith('#') and not re.search(r'(?:\$\.)+#$', t_idx):
                last_entry = last_entry[:-1]

        return And(And(self.equalities),And(self.inequalities),
                   And(self.conditions), And(self.call_conditions))
