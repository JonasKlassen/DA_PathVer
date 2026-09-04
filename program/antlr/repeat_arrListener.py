# Generated from repeat_arr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .repeat_arrParser import repeat_arrParser
else:
    from repeat_arrParser import repeat_arrParser

# This class defines a complete listener for a parse tree produced by repeat_arrParser.
class repeat_arrListener(ParseTreeListener):

    # Enter a parse tree produced by repeat_arrParser#program.
    def enterProgram(self, ctx:repeat_arrParser.ProgramContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#program.
    def exitProgram(self, ctx:repeat_arrParser.ProgramContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#varDecl.
    def enterVarDecl(self, ctx:repeat_arrParser.VarDeclContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#varDecl.
    def exitVarDecl(self, ctx:repeat_arrParser.VarDeclContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#functionDecl.
    def enterFunctionDecl(self, ctx:repeat_arrParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#functionDecl.
    def exitFunctionDecl(self, ctx:repeat_arrParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#paramList.
    def enterParamList(self, ctx:repeat_arrParser.ParamListContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#paramList.
    def exitParamList(self, ctx:repeat_arrParser.ParamListContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#varList.
    def enterVarList(self, ctx:repeat_arrParser.VarListContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#varList.
    def exitVarList(self, ctx:repeat_arrParser.VarListContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#stmt.
    def enterStmt(self, ctx:repeat_arrParser.StmtContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#stmt.
    def exitStmt(self, ctx:repeat_arrParser.StmtContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#call.
    def enterCall(self, ctx:repeat_arrParser.CallContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#call.
    def exitCall(self, ctx:repeat_arrParser.CallContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#argList.
    def enterArgList(self, ctx:repeat_arrParser.ArgListContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#argList.
    def exitArgList(self, ctx:repeat_arrParser.ArgListContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#arg.
    def enterArg(self, ctx:repeat_arrParser.ArgContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#arg.
    def exitArg(self, ctx:repeat_arrParser.ArgContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#assign.
    def enterAssign(self, ctx:repeat_arrParser.AssignContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#assign.
    def exitAssign(self, ctx:repeat_arrParser.AssignContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#ret.
    def enterRet(self, ctx:repeat_arrParser.RetContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#ret.
    def exitRet(self, ctx:repeat_arrParser.RetContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#ArithExpr.
    def enterArithExpr(self, ctx:repeat_arrParser.ArithExprContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#ArithExpr.
    def exitArithExpr(self, ctx:repeat_arrParser.ArithExprContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#ComparisonExpr.
    def enterComparisonExpr(self, ctx:repeat_arrParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#ComparisonExpr.
    def exitComparisonExpr(self, ctx:repeat_arrParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#ConnExpr.
    def enterConnExpr(self, ctx:repeat_arrParser.ConnExprContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#ConnExpr.
    def exitConnExpr(self, ctx:repeat_arrParser.ConnExprContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#AtomExpr.
    def enterAtomExpr(self, ctx:repeat_arrParser.AtomExprContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#AtomExpr.
    def exitAtomExpr(self, ctx:repeat_arrParser.AtomExprContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#LogicalExpr.
    def enterLogicalExpr(self, ctx:repeat_arrParser.LogicalExprContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#LogicalExpr.
    def exitLogicalExpr(self, ctx:repeat_arrParser.LogicalExprContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#IntAtom.
    def enterIntAtom(self, ctx:repeat_arrParser.IntAtomContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#IntAtom.
    def exitIntAtom(self, ctx:repeat_arrParser.IntAtomContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#TrueAtom.
    def enterTrueAtom(self, ctx:repeat_arrParser.TrueAtomContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#TrueAtom.
    def exitTrueAtom(self, ctx:repeat_arrParser.TrueAtomContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#FalseAtom.
    def enterFalseAtom(self, ctx:repeat_arrParser.FalseAtomContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#FalseAtom.
    def exitFalseAtom(self, ctx:repeat_arrParser.FalseAtomContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#VarAtom.
    def enterVarAtom(self, ctx:repeat_arrParser.VarAtomContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#VarAtom.
    def exitVarAtom(self, ctx:repeat_arrParser.VarAtomContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#IndexAtom.
    def enterIndexAtom(self, ctx:repeat_arrParser.IndexAtomContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#IndexAtom.
    def exitIndexAtom(self, ctx:repeat_arrParser.IndexAtomContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#ParenAtom.
    def enterParenAtom(self, ctx:repeat_arrParser.ParenAtomContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#ParenAtom.
    def exitParenAtom(self, ctx:repeat_arrParser.ParenAtomContext):
        pass


    # Enter a parse tree produced by repeat_arrParser#var.
    def enterVar(self, ctx:repeat_arrParser.VarContext):
        pass

    # Exit a parse tree produced by repeat_arrParser#var.
    def exitVar(self, ctx:repeat_arrParser.VarContext):
        pass



del repeat_arrParser