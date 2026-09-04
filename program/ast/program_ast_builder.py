from ..antlr.repeat_arrVisitor import repeat_arrVisitor
from .program_ast_nodes import *

class ProgramASTBuilder(repeat_arrVisitor):

    # ---------------- PROGRAM ----------------
    def visitProgram(self, ctx):
        local_vars = []
        global_vars = []
        for decl in ctx.varDecl():
            target = global_vars if decl.GLOBAL() else local_vars
            for var in decl.varList().var():
                name = var.getText()
                if name not in target:
                    target.append(name)

        overlap = set(local_vars) & set(global_vars)
        if overlap:
            names = ", ".join(sorted(overlap))
            raise ValueError(f"Variables declared as both local and global: {names}")

        functions = {}
        for f in ctx.functionDecl():
            func = self.visit(f)
            functions[func.name] = func
        program = Program(local_vars, global_vars, functions)
        self._validate_declared_variables(program)
        return program

    # ---------------- FUNCTION ----------------
    def visitFunctionDecl(self, ctx):
        name = int(ctx.INTEGER().getText())

        params = []
        if ctx.paramList():
            params = [v.getText() for v in ctx.paramList().varList().var()]

        body = []
        for i, s in enumerate(ctx.stmt()):
            stmt_node = self.visit(s)
            stmt_node.index = i
            body.append(stmt_node)

        return Function(name, params, body)

    def _validate_declared_variables(self, program):
        declared_vars = set(program.local_vars) | set(program.global_vars)
        for func in program.functions.values():
            for param in func.params:
                if param not in declared_vars:
                    raise ValueError(f"Parameter '{param}' in function {func.name} is not declared.")
                if param in program.global_vars:
                    raise ValueError(f"Global variable '{param}' cannot be a parameter of function {func.name}.")

            for stmt in func.body:
                for ref_arg in self._ref_args_in_node(stmt):
                    if ref_arg in program.global_vars:
                        raise ValueError(f"Global variable '{ref_arg}' cannot be passed as a ref argument.")
                for name in self._vars_in_node(stmt):
                    if name == "@fn":
                        continue
                    if name not in declared_vars:
                        raise ValueError(f"Variable '{name}' in function {func.name} is not declared.")

    def _vars_in_node(self, node):
        if isinstance(node, (Var, RefArg, Arg)):
            return {node.name}
        if isinstance(node, ArrayAccess):
            return {node.name} | self._vars_in_node(node.index)
        if isinstance(node, Assign):
            return self._vars_in_node(node.target) | self._vars_in_node(node.value)
        if isinstance(node, Call):
            vars_found = self._vars_in_node(node.expr)
            for arg in node.args:
                vars_found |= self._vars_in_node(arg)
            return vars_found
        if isinstance(node, Return):
            return self._vars_in_node(node.expr)
        if isinstance(node, BinOp):
            return self._vars_in_node(node.left) | self._vars_in_node(node.right)
        return set()

    def _ref_args_in_node(self, node):
        if isinstance(node, RefArg):
            return {node.name}
        if isinstance(node, Call):
            refs = set()
            for arg in node.args:
                refs |= self._ref_args_in_node(arg)
            return refs
        return set()

    # ---------------- STATEMENTS ----------------
    def visitAssign(self, ctx):
        target = ctx.var().getText()
        exprs = ctx.expr()

        # array assignment: var[expr] = expr
        if len(exprs) == 2:
            index = self.visit(exprs[0])
            value = self.visit(exprs[1])
            return Assign(ArrayAccess(target, index), value)

        # simple assignment: var = expr
        value = self.visit(exprs[0])
        return Assign(Var(target), value)

    def visitCall(self, ctx):
        # expr = ctx.expr().getText()
        expr = self.visit(ctx.expr())

        args = []
        if ctx.argList():
            args = [self.visit(a) for a in ctx.argList().arg()]

        return Call(expr, args)

    def visitRet(self, ctx):
        if ctx.expr():
            return Return(self.visit(ctx.expr()))
        return Return(AstBool(1))

    def visitStmt(self, ctx):
        if ctx.REPEAT():
            return Repeat()
        return self.visitChildren(ctx)


    # ---------------- ARGUMENTS ----------------
    def visitArg(self, ctx):
        if ctx.REF():
            return RefArg(ctx.var().getText())
        return Arg(ctx.var().getText())


    # ---------------- EXPRESSIONS ----------------

    def visitIntAtom(self, ctx):
        return AstInt(int(ctx.INTEGER().getText()))

    def visitTrueAtom(self, ctx):
        return AstBool(1)

    def visitFalseAtom(self, ctx):
        return AstBool(0)

    def visitVarAtom(self, ctx):
        return Var(ctx.var().getText())

    def visitIndexAtom(self, ctx):
        name = ctx.var().getText()
        index = self.visit(ctx.expr())
        return ArrayAccess(name, index)

    def visitParenAtom(self, ctx):
        return self.visit(ctx.expr())

    def visitComparisonExpr(self, ctx):
        op = ctx.getChild(1).getText()
        return BinOp(op, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitLogicalExpr(self, ctx):
        op = ctx.getChild(1).getText()
        return BinOp(op, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitArithExpr(self, ctx):
        op = ctx.getChild(1).getText()
        return BinOp(op, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitConnExpr(self, ctx):
        op = ctx.getChild(1).getText()
        return BinOp(op, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitAtomExpr(self, ctx):
        return self.visit(ctx.atom())
