# Generated from contract.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .contractParser import contractParser
else:
    from contractParser import contractParser

# This class defines a complete generic visitor for a parse tree produced by contractParser.

class contractVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by contractParser#init.
    def visitInit(self, ctx:contractParser.InitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by contractParser#contract.
    def visitContract(self, ctx:contractParser.ContractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by contractParser#trace.
    def visitTrace(self, ctx:contractParser.TraceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by contractParser#contract_atom.
    def visitContract_atom(self, ctx:contractParser.Contract_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by contractParser#indexed_var.
    def visitIndexed_var(self, ctx:contractParser.Indexed_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by contractParser#trace_atom.
    def visitTrace_atom(self, ctx:contractParser.Trace_atomContext):
        return self.visitChildren(ctx)



del contractParser