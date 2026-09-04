# Generated from repeat_arr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .repeat_arrParser import repeat_arrParser
else:
    from repeat_arrParser import repeat_arrParser

# This class defines a complete generic visitor for a parse tree produced by repeat_arrParser.

class repeat_arrVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by repeat_arrParser#program.
    def visitProgram(self, ctx:repeat_arrParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#varDecl.
    def visitVarDecl(self, ctx:repeat_arrParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#functionDecl.
    def visitFunctionDecl(self, ctx:repeat_arrParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#paramList.
    def visitParamList(self, ctx:repeat_arrParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#varList.
    def visitVarList(self, ctx:repeat_arrParser.VarListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#stmt.
    def visitStmt(self, ctx:repeat_arrParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#call.
    def visitCall(self, ctx:repeat_arrParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#argList.
    def visitArgList(self, ctx:repeat_arrParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#arg.
    def visitArg(self, ctx:repeat_arrParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#assign.
    def visitAssign(self, ctx:repeat_arrParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#ret.
    def visitRet(self, ctx:repeat_arrParser.RetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#ArithExpr.
    def visitArithExpr(self, ctx:repeat_arrParser.ArithExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#ComparisonExpr.
    def visitComparisonExpr(self, ctx:repeat_arrParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#ConnExpr.
    def visitConnExpr(self, ctx:repeat_arrParser.ConnExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#AtomExpr.
    def visitAtomExpr(self, ctx:repeat_arrParser.AtomExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#LogicalExpr.
    def visitLogicalExpr(self, ctx:repeat_arrParser.LogicalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#IntAtom.
    def visitIntAtom(self, ctx:repeat_arrParser.IntAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#TrueAtom.
    def visitTrueAtom(self, ctx:repeat_arrParser.TrueAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#FalseAtom.
    def visitFalseAtom(self, ctx:repeat_arrParser.FalseAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#VarAtom.
    def visitVarAtom(self, ctx:repeat_arrParser.VarAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#IndexAtom.
    def visitIndexAtom(self, ctx:repeat_arrParser.IndexAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#ParenAtom.
    def visitParenAtom(self, ctx:repeat_arrParser.ParenAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by repeat_arrParser#var.
    def visitVar(self, ctx:repeat_arrParser.VarContext):
        return self.visitChildren(ctx)



del repeat_arrParser