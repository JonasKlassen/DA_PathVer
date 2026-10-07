# Generated from property.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,31,97,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,
        0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,45,
        8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,56,8,1,10,1,12,1,59,
        9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,74,8,
        2,1,2,1,2,1,2,5,2,79,8,2,10,2,12,2,82,9,2,1,3,1,3,1,3,1,3,3,3,88,
        8,3,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,0,2,2,4,6,0,2,4,6,8,10,0,6,1,
        0,29,30,1,0,13,18,1,0,8,9,1,0,10,11,1,0,26,27,2,0,21,24,26,26,104,
        0,12,1,0,0,0,2,44,1,0,0,0,4,73,1,0,0,0,6,87,1,0,0,0,8,89,1,0,0,0,
        10,94,1,0,0,0,12,13,3,2,1,0,13,14,5,0,0,1,14,1,1,0,0,0,15,16,6,1,
        -1,0,16,17,5,5,0,0,17,18,3,2,1,0,18,19,5,6,0,0,19,45,1,0,0,0,20,
        21,7,0,0,0,21,22,5,27,0,0,22,23,5,28,0,0,23,24,5,5,0,0,24,25,3,2,
        1,0,25,26,5,6,0,0,26,45,1,0,0,0,27,28,5,7,0,0,28,45,3,2,1,6,29,30,
        5,1,0,0,30,31,3,4,2,0,31,32,5,2,0,0,32,33,5,5,0,0,33,34,3,2,1,0,
        34,35,5,6,0,0,35,45,1,0,0,0,36,37,5,3,0,0,37,38,3,4,2,0,38,39,5,
        4,0,0,39,40,5,5,0,0,40,41,3,2,1,0,41,42,5,6,0,0,42,45,1,0,0,0,43,
        45,3,6,3,0,44,15,1,0,0,0,44,20,1,0,0,0,44,27,1,0,0,0,44,29,1,0,0,
        0,44,36,1,0,0,0,44,43,1,0,0,0,45,57,1,0,0,0,46,47,10,7,0,0,47,48,
        7,1,0,0,48,56,3,2,1,8,49,50,10,5,0,0,50,51,7,2,0,0,51,56,3,2,1,6,
        52,53,10,4,0,0,53,54,7,3,0,0,54,56,3,2,1,5,55,46,1,0,0,0,55,49,1,
        0,0,0,55,52,1,0,0,0,56,59,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,
        3,1,0,0,0,59,57,1,0,0,0,60,61,6,2,-1,0,61,62,5,5,0,0,62,63,3,4,2,
        0,63,64,5,6,0,0,64,65,5,20,0,0,65,74,1,0,0,0,66,67,5,5,0,0,67,68,
        3,4,2,0,68,69,5,12,0,0,69,70,3,4,2,0,70,71,5,6,0,0,71,74,1,0,0,0,
        72,74,3,10,5,0,73,60,1,0,0,0,73,66,1,0,0,0,73,72,1,0,0,0,74,80,1,
        0,0,0,75,76,10,2,0,0,76,77,5,19,0,0,77,79,3,4,2,3,78,75,1,0,0,0,
        79,82,1,0,0,0,80,78,1,0,0,0,80,81,1,0,0,0,81,5,1,0,0,0,82,80,1,0,
        0,0,83,88,5,27,0,0,84,88,3,8,4,0,85,88,5,25,0,0,86,88,5,26,0,0,87,
        83,1,0,0,0,87,84,1,0,0,0,87,85,1,0,0,0,87,86,1,0,0,0,88,7,1,0,0,
        0,89,90,5,27,0,0,90,91,5,1,0,0,91,92,7,4,0,0,92,93,5,2,0,0,93,9,
        1,0,0,0,94,95,7,5,0,0,95,11,1,0,0,0,6,44,55,57,73,80,87
    ]

class propertyParser ( Parser ):

    grammarFileName = "property.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "']'", "'{'", "'}'", "'('", "')'", 
                     "'!'", "'&'", "'|'", "'=>'", "'<=>'", "'U'", "'<='", 
                     "'=='", "'<'", "'!='", "'>='", "'>'", "'.'", "'*'", 
                     "'?'", "'$'", "'#'", "'eps'", "'@fn'", "<INVALID>", 
                     "<INVALID>", "':'", "'EXISTS'", "'FORALL'" ]

    symbolicNames = [ "<INVALID>", "LBRACKET", "RBRACKET", "LDIAMOND", "RDIAMOND", 
                      "LPAREN", "RPAREN", "NOT", "AND", "OR", "IMPL", "EQUIV", 
                      "CUP", "LE", "EQ", "LT", "NEQ", "GE", "GT", "DOT", 
                      "KLEENE", "WILDCARD", "DOLLAR", "HASHTAG", "EPSILON", 
                      "ATFN", "INT", "VAR", "COLON", "EXISTS", "FORALL", 
                      "WS" ]

    RULE_init = 0
    RULE_property = 1
    RULE_trace = 2
    RULE_property_atom = 3
    RULE_indexed_var = 4
    RULE_trace_atom = 5

    ruleNames =  [ "init", "property", "trace", "property_atom", "indexed_var", 
                   "trace_atom" ]

    EOF = Token.EOF
    LBRACKET=1
    RBRACKET=2
    LDIAMOND=3
    RDIAMOND=4
    LPAREN=5
    RPAREN=6
    NOT=7
    AND=8
    OR=9
    IMPL=10
    EQUIV=11
    CUP=12
    LE=13
    EQ=14
    LT=15
    NEQ=16
    GE=17
    GT=18
    DOT=19
    KLEENE=20
    WILDCARD=21
    DOLLAR=22
    HASHTAG=23
    EPSILON=24
    ATFN=25
    INT=26
    VAR=27
    COLON=28
    EXISTS=29
    FORALL=30
    WS=31

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class InitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def property_(self):
            return self.getTypedRuleContext(propertyParser.PropertyContext,0)


        def EOF(self):
            return self.getToken(propertyParser.EOF, 0)

        def getRuleIndex(self):
            return propertyParser.RULE_init

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInit" ):
                listener.enterInit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInit" ):
                listener.exitInit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInit" ):
                return visitor.visitInit(self)
            else:
                return visitor.visitChildren(self)




    def init(self):

        localctx = propertyParser.InitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_init)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.property_(0)
            self.state = 13
            self.match(propertyParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(propertyParser.LPAREN, 0)

        def property_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(propertyParser.PropertyContext)
            else:
                return self.getTypedRuleContext(propertyParser.PropertyContext,i)


        def RPAREN(self):
            return self.getToken(propertyParser.RPAREN, 0)

        def VAR(self):
            return self.getToken(propertyParser.VAR, 0)

        def COLON(self):
            return self.getToken(propertyParser.COLON, 0)

        def EXISTS(self):
            return self.getToken(propertyParser.EXISTS, 0)

        def FORALL(self):
            return self.getToken(propertyParser.FORALL, 0)

        def NOT(self):
            return self.getToken(propertyParser.NOT, 0)

        def LBRACKET(self):
            return self.getToken(propertyParser.LBRACKET, 0)

        def trace(self):
            return self.getTypedRuleContext(propertyParser.TraceContext,0)


        def RBRACKET(self):
            return self.getToken(propertyParser.RBRACKET, 0)

        def LDIAMOND(self):
            return self.getToken(propertyParser.LDIAMOND, 0)

        def RDIAMOND(self):
            return self.getToken(propertyParser.RDIAMOND, 0)

        def property_atom(self):
            return self.getTypedRuleContext(propertyParser.Property_atomContext,0)


        def EQ(self):
            return self.getToken(propertyParser.EQ, 0)

        def LE(self):
            return self.getToken(propertyParser.LE, 0)

        def LT(self):
            return self.getToken(propertyParser.LT, 0)

        def NEQ(self):
            return self.getToken(propertyParser.NEQ, 0)

        def GE(self):
            return self.getToken(propertyParser.GE, 0)

        def GT(self):
            return self.getToken(propertyParser.GT, 0)

        def AND(self):
            return self.getToken(propertyParser.AND, 0)

        def OR(self):
            return self.getToken(propertyParser.OR, 0)

        def IMPL(self):
            return self.getToken(propertyParser.IMPL, 0)

        def EQUIV(self):
            return self.getToken(propertyParser.EQUIV, 0)

        def getRuleIndex(self):
            return propertyParser.RULE_property

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProperty" ):
                listener.enterProperty(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProperty" ):
                listener.exitProperty(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProperty" ):
                return visitor.visitProperty(self)
            else:
                return visitor.visitChildren(self)



    def property_(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = propertyParser.PropertyContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_property, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.state = 16
                self.match(propertyParser.LPAREN)
                self.state = 17
                self.property_(0)
                self.state = 18
                self.match(propertyParser.RPAREN)
                pass
            elif token in [29, 30]:
                self.state = 20
                _la = self._input.LA(1)
                if not(_la==29 or _la==30):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 21
                self.match(propertyParser.VAR)
                self.state = 22
                self.match(propertyParser.COLON)
                self.state = 23
                self.match(propertyParser.LPAREN)
                self.state = 24
                self.property_(0)
                self.state = 25
                self.match(propertyParser.RPAREN)
                pass
            elif token in [7]:
                self.state = 27
                self.match(propertyParser.NOT)
                self.state = 28
                self.property_(6)
                pass
            elif token in [1]:
                self.state = 29
                self.match(propertyParser.LBRACKET)
                self.state = 30
                self.trace(0)
                self.state = 31
                self.match(propertyParser.RBRACKET)
                self.state = 32
                self.match(propertyParser.LPAREN)
                self.state = 33
                self.property_(0)
                self.state = 34
                self.match(propertyParser.RPAREN)
                pass
            elif token in [3]:
                self.state = 36
                self.match(propertyParser.LDIAMOND)
                self.state = 37
                self.trace(0)
                self.state = 38
                self.match(propertyParser.RDIAMOND)
                self.state = 39
                self.match(propertyParser.LPAREN)
                self.state = 40
                self.property_(0)
                self.state = 41
                self.match(propertyParser.RPAREN)
                pass
            elif token in [25, 26, 27]:
                self.state = 43
                self.property_atom()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 57
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 55
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = propertyParser.PropertyContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_property)
                        self.state = 46
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 47
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 516096) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 48
                        self.property_(8)
                        pass

                    elif la_ == 2:
                        localctx = propertyParser.PropertyContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_property)
                        self.state = 49
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 50
                        _la = self._input.LA(1)
                        if not(_la==8 or _la==9):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 51
                        self.property_(6)
                        pass

                    elif la_ == 3:
                        localctx = propertyParser.PropertyContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_property)
                        self.state = 52
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 53
                        _la = self._input.LA(1)
                        if not(_la==10 or _la==11):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 54
                        self.property_(5)
                        pass

             
                self.state = 59
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TraceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(propertyParser.LPAREN, 0)

        def trace(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(propertyParser.TraceContext)
            else:
                return self.getTypedRuleContext(propertyParser.TraceContext,i)


        def RPAREN(self):
            return self.getToken(propertyParser.RPAREN, 0)

        def KLEENE(self):
            return self.getToken(propertyParser.KLEENE, 0)

        def CUP(self):
            return self.getToken(propertyParser.CUP, 0)

        def trace_atom(self):
            return self.getTypedRuleContext(propertyParser.Trace_atomContext,0)


        def DOT(self):
            return self.getToken(propertyParser.DOT, 0)

        def getRuleIndex(self):
            return propertyParser.RULE_trace

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrace" ):
                listener.enterTrace(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrace" ):
                listener.exitTrace(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrace" ):
                return visitor.visitTrace(self)
            else:
                return visitor.visitChildren(self)



    def trace(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = propertyParser.TraceContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_trace, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 61
                self.match(propertyParser.LPAREN)
                self.state = 62
                self.trace(0)
                self.state = 63
                self.match(propertyParser.RPAREN)
                self.state = 64
                self.match(propertyParser.KLEENE)
                pass

            elif la_ == 2:
                self.state = 66
                self.match(propertyParser.LPAREN)
                self.state = 67
                self.trace(0)
                self.state = 68
                self.match(propertyParser.CUP)
                self.state = 69
                self.trace(0)
                self.state = 70
                self.match(propertyParser.RPAREN)
                pass

            elif la_ == 3:
                self.state = 72
                self.trace_atom()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 80
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = propertyParser.TraceContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_trace)
                    self.state = 75
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 76
                    self.match(propertyParser.DOT)
                    self.state = 77
                    self.trace(3) 
                self.state = 82
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Property_atomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(propertyParser.VAR, 0)

        def indexed_var(self):
            return self.getTypedRuleContext(propertyParser.Indexed_varContext,0)


        def ATFN(self):
            return self.getToken(propertyParser.ATFN, 0)

        def INT(self):
            return self.getToken(propertyParser.INT, 0)

        def getRuleIndex(self):
            return propertyParser.RULE_property_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProperty_atom" ):
                listener.enterProperty_atom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProperty_atom" ):
                listener.exitProperty_atom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProperty_atom" ):
                return visitor.visitProperty_atom(self)
            else:
                return visitor.visitChildren(self)




    def property_atom(self):

        localctx = propertyParser.Property_atomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_property_atom)
        try:
            self.state = 87
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 83
                self.match(propertyParser.VAR)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 84
                self.indexed_var()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 85
                self.match(propertyParser.ATFN)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 86
                self.match(propertyParser.INT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Indexed_varContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self, i:int=None):
            if i is None:
                return self.getTokens(propertyParser.VAR)
            else:
                return self.getToken(propertyParser.VAR, i)

        def LBRACKET(self):
            return self.getToken(propertyParser.LBRACKET, 0)

        def RBRACKET(self):
            return self.getToken(propertyParser.RBRACKET, 0)

        def INT(self):
            return self.getToken(propertyParser.INT, 0)

        def getRuleIndex(self):
            return propertyParser.RULE_indexed_var

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndexed_var" ):
                listener.enterIndexed_var(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndexed_var" ):
                listener.exitIndexed_var(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndexed_var" ):
                return visitor.visitIndexed_var(self)
            else:
                return visitor.visitChildren(self)




    def indexed_var(self):

        localctx = propertyParser.Indexed_varContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_indexed_var)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(propertyParser.VAR)
            self.state = 90
            self.match(propertyParser.LBRACKET)
            self.state = 91
            _la = self._input.LA(1)
            if not(_la==26 or _la==27):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 92
            self.match(propertyParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Trace_atomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WILDCARD(self):
            return self.getToken(propertyParser.WILDCARD, 0)

        def DOLLAR(self):
            return self.getToken(propertyParser.DOLLAR, 0)

        def HASHTAG(self):
            return self.getToken(propertyParser.HASHTAG, 0)

        def INT(self):
            return self.getToken(propertyParser.INT, 0)

        def EPSILON(self):
            return self.getToken(propertyParser.EPSILON, 0)

        def getRuleIndex(self):
            return propertyParser.RULE_trace_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrace_atom" ):
                listener.enterTrace_atom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrace_atom" ):
                listener.exitTrace_atom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrace_atom" ):
                return visitor.visitTrace_atom(self)
            else:
                return visitor.visitChildren(self)




    def trace_atom(self):

        localctx = propertyParser.Trace_atomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_trace_atom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 98566144) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.property_sempred
        self._predicates[2] = self.trace_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def property_sempred(self, localctx:PropertyContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         

    def trace_sempred(self, localctx:TraceContext, predIndex:int):
            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         




