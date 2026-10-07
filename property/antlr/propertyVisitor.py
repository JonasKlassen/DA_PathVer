# Generated from property.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .propertyParser import propertyParser
else:
    from propertyParser import propertyParser

# This class defines a complete generic visitor for a parse tree produced by propertyParser.

class propertyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by propertyParser#init.
    def visitInit(self, ctx:propertyParser.InitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by propertyParser#property.
    def visitProperty(self, ctx:propertyParser.PropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by propertyParser#trace.
    def visitTrace(self, ctx:propertyParser.TraceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by propertyParser#property_atom.
    def visitProperty_atom(self, ctx:propertyParser.Property_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by propertyParser#indexed_var.
    def visitIndexed_var(self, ctx:propertyParser.Indexed_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by propertyParser#trace_atom.
    def visitTrace_atom(self, ctx:propertyParser.Trace_atomContext):
        return self.visitChildren(ctx)



del propertyParser