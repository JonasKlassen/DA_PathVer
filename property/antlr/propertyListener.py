# Generated from property.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .propertyParser import propertyParser
else:
    from propertyParser import propertyParser

# This class defines a complete listener for a parse tree produced by propertyParser.
class propertyListener(ParseTreeListener):

    # Enter a parse tree produced by propertyParser#init.
    def enterInit(self, ctx:propertyParser.InitContext):
        pass

    # Exit a parse tree produced by propertyParser#init.
    def exitInit(self, ctx:propertyParser.InitContext):
        pass


    # Enter a parse tree produced by propertyParser#property.
    def enterProperty(self, ctx:propertyParser.PropertyContext):
        pass

    # Exit a parse tree produced by propertyParser#property.
    def exitProperty(self, ctx:propertyParser.PropertyContext):
        pass


    # Enter a parse tree produced by propertyParser#trace.
    def enterTrace(self, ctx:propertyParser.TraceContext):
        pass

    # Exit a parse tree produced by propertyParser#trace.
    def exitTrace(self, ctx:propertyParser.TraceContext):
        pass


    # Enter a parse tree produced by propertyParser#property_atom.
    def enterProperty_atom(self, ctx:propertyParser.Property_atomContext):
        pass

    # Exit a parse tree produced by propertyParser#property_atom.
    def exitProperty_atom(self, ctx:propertyParser.Property_atomContext):
        pass


    # Enter a parse tree produced by propertyParser#indexed_var.
    def enterIndexed_var(self, ctx:propertyParser.Indexed_varContext):
        pass

    # Exit a parse tree produced by propertyParser#indexed_var.
    def exitIndexed_var(self, ctx:propertyParser.Indexed_varContext):
        pass


    # Enter a parse tree produced by propertyParser#trace_atom.
    def enterTrace_atom(self, ctx:propertyParser.Trace_atomContext):
        pass

    # Exit a parse tree produced by propertyParser#trace_atom.
    def exitTrace_atom(self, ctx:propertyParser.Trace_atomContext):
        pass



del propertyParser