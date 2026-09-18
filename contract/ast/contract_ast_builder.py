from DA_PathVer.contract.antlr.contractVisitor import contractVisitor
from DA_PathVer.contract.ast.contract_ast_nodes import *

class ContractASTBuilder(contractVisitor):

    def visitInit(self, ctx):
        return Init(self.visit(ctx.contract()))

    def visitContract(self, ctx):
        if ctx.LBRACKET():
            return Modal("BOX", self.visit(ctx.trace()), self.visit(ctx.contract(0)))
        if ctx.LDIAMOND():
            return Modal("DIAMOND", self.visit(ctx.trace()), self.visit(ctx.contract(0)))
        if ctx.EXISTS():
            return Quantifier("EXISTS", ctx.VAR().getText(), self.visit(ctx.contract(0)))
        if ctx.FORALL():
            return Quantifier("FORALL", ctx.VAR().getText(), self.visit(ctx.contract(0)))
        if ctx.LPAREN():
            return self.visit(ctx.contract(0))
        if ctx.NOT():
            return UnOp("NOT", self.visit(ctx.contract(0)))
        if ctx.AND():
            return BinOp("AND", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.OR():
            return BinOp("OR", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.IMPL():
            return BinOp("IMPL", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.EQUIV():
            return BinOp("EQUIV", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.LT():
            return BinOp("LT", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.LE():
            return BinOp("LE", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.EQ():
            return BinOp("EQ", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.GT():
            return BinOp("GT", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.GE():
            return BinOp("GE", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        if ctx.NEQ():
            return BinOp("NEQ", self.visit(ctx.contract(0)), self.visit(ctx.contract(1)))
        return self.visit(ctx.contract_atom())

    def visitContract_atom(self, ctx):
        if ctx.VAR():
            return Var(ctx.VAR().getText(), None)
        if ctx.indexed_var():
            var_name = ctx.indexed_var().VAR(0).getText()
            if ctx.indexed_var().INT():
                return Var(var_name, int(ctx.indexed_var().INT().getText()))
            else:
                return Var(var_name, ctx.indexed_var().VAR(1).getText())
        if ctx.ATFN():
            return AtFn()
        return AstInt(int(ctx.INT().getText()))

    def visitTrace(self, ctx):
        if ctx.KLEENE():
            return UnOp("KLEENE", self.visit(ctx.trace(0)))
        if ctx.CUP():
            return BinOp("CUP", self.visit(ctx.trace(0)), self.visit(ctx.trace(1)))
        if ctx.DOT():
            return BinOp("DOT", self.visit(ctx.trace(0)), self.visit(ctx.trace(1)))
        return self.visit(ctx.trace_atom())

    def visitTrace_atom(self, ctx):
        if ctx.WILDCARD():
            return TraceAtom("?")
        if ctx.DOLLAR():
            return TraceAtom("$")
        if ctx.HASHTAG():
            return TraceAtom("#")
        if ctx.EPSILON():
            return TraceAtom("eps")
        return AstInt(int(ctx.INT().getText()))