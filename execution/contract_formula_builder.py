from pysmt.shortcuts import And, Or, Not, Implies, Iff, Equals, LE, Int, Select, TRUE, FALSE, LT, NotEquals, GE, GT, Exists, ForAll, Symbol
from pysmt.typing import INT
import re

from repeat_arr_verifier.contract.ast.contract_ast_nodes import *


class ContractFormulaBuilder:
    def __init__(self, trace_info, idx_vars):
        self.trace_info = trace_info  # List of (t_idx, f_name, stmt)
        self.trace_indices = [t[0] for t in trace_info]
        self.idx_vars = idx_vars  # var -> t_idx -> [curr_sym, prev_sym]

    def resolve_formula(self, ast):
        return self._visit(ast, '', {})

    def _visit(self, node, trace, scope):
        if isinstance(node, Modal):
            if trace == '':
                trace_regex = "^" + self._visit_trace(node.trace) + "$"
            else:
                trace_regex = "^" + trace + '\\.' + self._visit_trace(node.trace) + "$"
            matched_trace_indices = [t_idx for t_idx in self.trace_indices if re.match(trace_regex, t_idx)]
            formulas = []
            for matched_trace in matched_trace_indices:
                formula = self._visit(node.contract, matched_trace, scope)
                if formula is not None:
                    formulas.append(formula)
            if len(formulas) == 0: return None
            elif node.mode == 'BOX': return And(*formulas)
            else: return Or(*formulas)
        elif isinstance(node, BinOp):
            left = self._visit(node.left, trace, scope)
            right = self._visit(node.right, trace, scope)
            if left is None or right is None: return FALSE()
            if node.op == 'AND': return And(left, right)
            if node.op == 'OR': return Or(left, right)
            if node.op == 'IMPL': return Implies(left, right)
            if node.op == 'EQUIV': return Iff(left, right)
            # Boolean atoms operations
            if node.op == 'LE': return LE(left, right)
            if node.op == 'EQ': return Equals(left, right)
            if node.op == 'LT': return LT(left, right)
            if node.op == 'GE': return GE(left, right)
            if node.op == 'NEQ': return NotEquals(left, right)
            if node.op == 'GT': return GT(left, right)
        elif isinstance(node, UnOp):
            operand = self._visit(node.value, trace, scope)
            if node.op == 'NOT': return Not(operand)
        elif isinstance(node, Quantifier):
            if node.var in self.idx_vars:
                raise ValueError(f"Quantified variable '{node.var}' conflicts with an existing program variable.")
            if node.var in scope:
                raise ValueError(f"Quantified variable '{node.var}' is already defined in an outer scope.")
            qvar = Symbol(node.var, INT)
            new_scope = scope.copy()
            new_scope[node.var] = qvar
            formula = self._visit(node.contract, trace, new_scope)
            if node.qtype == 'EXISTS': return Exists([qvar], formula)
            else: return ForAll([qvar], formula)
        elif isinstance(node, Var):
            if node.name in scope:
                return scope[node.name]
            if trace == '': trace = 'epsilon'
            sym = self.idx_vars[node.name][trace][0]
            idx = Int(0)
            if node.index is not None:
                if isinstance(node.index, int):
                    idx = Int(node.index)
                elif isinstance(node.index, str):
                    if node.index in scope:
                        idx = scope[node.index]
                    else:
                        # This shouldn't happen if the contract is well-formed
                        # But maybe it's a program variable? Not supported as index here yet.
                        idx = Int(0) 
            return Select(sym, idx)
        elif isinstance(node, AstInt):
            return Int(node.value)
        elif isinstance(node, AtFn):
            return self.idx_vars['@fn'][trace][0]
        return None


    def _visit_trace(self, trace):
        if isinstance(trace, BinOp):
            if trace.op == 'DOT':
                return f"{self._visit_trace(trace.left)}\\.{self._visit_trace(trace.right)}"
            if trace.op == 'CUP':
                return f"({self._visit_trace(trace.left)}|{self._visit_trace(trace.right)})"
        if isinstance(trace, UnOp):
            if trace.op == 'KLEENE':
                val = self._visit_trace(trace.value)
                return f"{val}(\\.{val})*"
        if isinstance(trace, TraceAtom) or isinstance(trace, AstInt):
            if trace.value == '$': return '[$]'
            if trace.value == '?': return '.'
            return str(trace.value)
        return None

