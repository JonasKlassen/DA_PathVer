# Generated from contract.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .contractParser import contractParser
else:
    from contractParser import contractParser

# This class defines a complete listener for a parse tree produced by contractParser.
class contractListener(ParseTreeListener):

    # Enter a parse tree produced by contractParser#init.
    def enterInit(self, ctx:contractParser.InitContext):
        pass

    # Exit a parse tree produced by contractParser#init.
    def exitInit(self, ctx:contractParser.InitContext):
        pass


    # Enter a parse tree produced by contractParser#contract.
    def enterContract(self, ctx:contractParser.ContractContext):
        pass

    # Exit a parse tree produced by contractParser#contract.
    def exitContract(self, ctx:contractParser.ContractContext):
        pass


    # Enter a parse tree produced by contractParser#trace.
    def enterTrace(self, ctx:contractParser.TraceContext):
        pass

    # Exit a parse tree produced by contractParser#trace.
    def exitTrace(self, ctx:contractParser.TraceContext):
        pass


    # Enter a parse tree produced by contractParser#contract_atom.
    def enterContract_atom(self, ctx:contractParser.Contract_atomContext):
        pass

    # Exit a parse tree produced by contractParser#contract_atom.
    def exitContract_atom(self, ctx:contractParser.Contract_atomContext):
        pass


    # Enter a parse tree produced by contractParser#indexed_var.
    def enterIndexed_var(self, ctx:contractParser.Indexed_varContext):
        pass

    # Exit a parse tree produced by contractParser#indexed_var.
    def exitIndexed_var(self, ctx:contractParser.Indexed_varContext):
        pass


    # Enter a parse tree produced by contractParser#trace_atom.
    def enterTrace_atom(self, ctx:contractParser.Trace_atomContext):
        pass

    # Exit a parse tree produced by contractParser#trace_atom.
    def exitTrace_atom(self, ctx:contractParser.Trace_atomContext):
        pass



del contractParser