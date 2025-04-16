# Generated from Rust.g4 by ANTLR 4.13.1
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
        4,1,48,278,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,1,0,4,0,48,8,0,11,0,12,0,49,1,1,1,1,1,1,
        1,1,3,1,56,8,1,1,1,1,1,3,1,60,8,1,1,1,3,1,63,8,1,1,1,1,1,1,2,1,2,
        1,2,5,2,70,8,2,10,2,12,2,73,9,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,5,
        1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,
        1,5,3,5,100,8,5,1,6,1,6,5,6,104,8,6,10,6,12,6,107,9,6,1,6,3,6,110,
        8,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,3,7,119,8,7,1,8,1,8,3,8,123,8,8,
        1,8,1,8,1,8,3,8,128,8,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,10,
        1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,3,11,150,8,11,
        1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,3,13,160,8,13,1,14,1,14,
        1,14,1,14,1,14,1,14,1,14,1,14,1,14,3,14,171,8,14,1,14,3,14,174,8,
        14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,
        14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,3,
        14,201,8,14,1,14,5,14,204,8,14,10,14,12,14,207,9,14,1,15,1,15,1,
        15,1,15,1,15,3,15,214,8,15,1,15,1,15,1,15,1,15,1,15,3,15,221,8,15,
        1,16,1,16,1,16,5,16,226,8,16,10,16,12,16,229,9,16,1,17,1,17,1,17,
        1,17,1,18,1,18,3,18,237,8,18,1,18,1,18,1,18,3,18,242,8,18,1,18,3,
        18,245,8,18,1,19,1,19,1,19,3,19,250,8,19,1,20,1,20,1,20,1,20,3,20,
        256,8,20,1,21,1,21,1,21,1,21,5,21,262,8,21,10,21,12,21,265,9,21,
        1,21,1,21,1,22,1,22,5,22,271,8,22,10,22,12,22,274,9,22,1,22,1,22,
        1,22,1,272,1,28,23,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,
        34,36,38,40,42,44,0,2,2,0,7,7,26,31,1,0,34,41,299,0,47,1,0,0,0,2,
        51,1,0,0,0,4,66,1,0,0,0,6,74,1,0,0,0,8,78,1,0,0,0,10,99,1,0,0,0,
        12,101,1,0,0,0,14,118,1,0,0,0,16,120,1,0,0,0,18,133,1,0,0,0,20,138,
        1,0,0,0,22,144,1,0,0,0,24,151,1,0,0,0,26,159,1,0,0,0,28,173,1,0,
        0,0,30,220,1,0,0,0,32,222,1,0,0,0,34,230,1,0,0,0,36,244,1,0,0,0,
        38,246,1,0,0,0,40,255,1,0,0,0,42,257,1,0,0,0,44,268,1,0,0,0,46,48,
        3,2,1,0,47,46,1,0,0,0,48,49,1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,
        50,1,1,0,0,0,51,52,5,1,0,0,52,53,5,45,0,0,53,55,5,2,0,0,54,56,3,
        4,2,0,55,54,1,0,0,0,55,56,1,0,0,0,56,57,1,0,0,0,57,59,5,3,0,0,58,
        60,5,4,0,0,59,58,1,0,0,0,59,60,1,0,0,0,60,62,1,0,0,0,61,63,3,10,
        5,0,62,61,1,0,0,0,62,63,1,0,0,0,63,64,1,0,0,0,64,65,3,12,6,0,65,
        3,1,0,0,0,66,71,3,6,3,0,67,68,5,5,0,0,68,70,3,6,3,0,69,67,1,0,0,
        0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,5,1,0,0,0,73,71,1,
        0,0,0,74,75,5,45,0,0,75,76,5,6,0,0,76,77,3,8,4,0,77,7,1,0,0,0,78,
        79,5,7,0,0,79,80,3,10,5,0,80,9,1,0,0,0,81,100,5,8,0,0,82,83,5,9,
        0,0,83,84,5,10,0,0,84,85,3,10,5,0,85,86,5,11,0,0,86,100,1,0,0,0,
        87,88,5,7,0,0,88,100,3,10,5,0,89,90,5,12,0,0,90,91,3,10,5,0,91,92,
        5,13,0,0,92,93,5,46,0,0,93,94,5,14,0,0,94,100,1,0,0,0,95,96,5,12,
        0,0,96,97,3,10,5,0,97,98,5,14,0,0,98,100,1,0,0,0,99,81,1,0,0,0,99,
        82,1,0,0,0,99,87,1,0,0,0,99,89,1,0,0,0,99,95,1,0,0,0,100,11,1,0,
        0,0,101,105,5,15,0,0,102,104,3,14,7,0,103,102,1,0,0,0,104,107,1,
        0,0,0,105,103,1,0,0,0,105,106,1,0,0,0,106,109,1,0,0,0,107,105,1,
        0,0,0,108,110,3,26,13,0,109,108,1,0,0,0,109,110,1,0,0,0,110,111,
        1,0,0,0,111,112,5,16,0,0,112,13,1,0,0,0,113,119,3,16,8,0,114,119,
        3,18,9,0,115,119,3,20,10,0,116,119,3,22,11,0,117,119,3,24,12,0,118,
        113,1,0,0,0,118,114,1,0,0,0,118,115,1,0,0,0,118,116,1,0,0,0,118,
        117,1,0,0,0,119,15,1,0,0,0,120,122,5,17,0,0,121,123,5,18,0,0,122,
        121,1,0,0,0,122,123,1,0,0,0,123,124,1,0,0,0,124,127,5,45,0,0,125,
        126,5,6,0,0,126,128,3,10,5,0,127,125,1,0,0,0,127,128,1,0,0,0,128,
        129,1,0,0,0,129,130,5,19,0,0,130,131,3,28,14,0,131,132,5,13,0,0,
        132,17,1,0,0,0,133,134,3,28,14,0,134,135,5,19,0,0,135,136,3,28,14,
        0,136,137,5,13,0,0,137,19,1,0,0,0,138,139,5,20,0,0,139,140,5,45,
        0,0,140,141,5,21,0,0,141,142,3,28,14,0,142,143,3,12,6,0,143,21,1,
        0,0,0,144,145,5,22,0,0,145,146,3,28,14,0,146,149,3,12,6,0,147,148,
        5,23,0,0,148,150,3,12,6,0,149,147,1,0,0,0,149,150,1,0,0,0,150,23,
        1,0,0,0,151,152,3,28,14,0,152,153,5,13,0,0,153,25,1,0,0,0,154,155,
        5,24,0,0,155,156,3,28,14,0,156,157,5,13,0,0,157,160,1,0,0,0,158,
        160,3,28,14,0,159,154,1,0,0,0,159,158,1,0,0,0,160,27,1,0,0,0,161,
        162,6,14,-1,0,162,174,3,30,15,0,163,174,3,34,17,0,164,165,5,7,0,
        0,165,174,3,28,14,9,166,167,5,45,0,0,167,168,5,42,0,0,168,170,5,
        2,0,0,169,171,3,32,16,0,170,169,1,0,0,0,170,171,1,0,0,0,171,172,
        1,0,0,0,172,174,5,3,0,0,173,161,1,0,0,0,173,163,1,0,0,0,173,164,
        1,0,0,0,173,166,1,0,0,0,174,205,1,0,0,0,175,176,10,5,0,0,176,177,
        7,0,0,0,177,204,3,28,14,6,178,179,10,4,0,0,179,180,5,32,0,0,180,
        204,3,28,14,5,181,182,10,3,0,0,182,183,5,33,0,0,183,204,3,28,14,
        4,184,185,10,2,0,0,185,186,7,1,0,0,186,204,3,28,14,3,187,188,10,
        8,0,0,188,189,5,12,0,0,189,190,3,28,14,0,190,191,5,14,0,0,191,204,
        1,0,0,0,192,193,10,7,0,0,193,194,5,25,0,0,194,204,5,45,0,0,195,196,
        10,6,0,0,196,197,5,25,0,0,197,198,5,45,0,0,198,200,5,2,0,0,199,201,
        3,32,16,0,200,199,1,0,0,0,200,201,1,0,0,0,201,202,1,0,0,0,202,204,
        5,3,0,0,203,175,1,0,0,0,203,178,1,0,0,0,203,181,1,0,0,0,203,184,
        1,0,0,0,203,187,1,0,0,0,203,192,1,0,0,0,203,195,1,0,0,0,204,207,
        1,0,0,0,205,203,1,0,0,0,205,206,1,0,0,0,206,29,1,0,0,0,207,205,1,
        0,0,0,208,221,3,40,20,0,209,221,5,45,0,0,210,211,5,45,0,0,211,213,
        5,2,0,0,212,214,3,32,16,0,213,212,1,0,0,0,213,214,1,0,0,0,214,215,
        1,0,0,0,215,221,5,3,0,0,216,217,5,2,0,0,217,218,3,28,14,0,218,219,
        5,3,0,0,219,221,1,0,0,0,220,208,1,0,0,0,220,209,1,0,0,0,220,210,
        1,0,0,0,220,216,1,0,0,0,221,31,1,0,0,0,222,227,3,28,14,0,223,224,
        5,5,0,0,224,226,3,28,14,0,225,223,1,0,0,0,226,229,1,0,0,0,227,225,
        1,0,0,0,227,228,1,0,0,0,228,33,1,0,0,0,229,227,1,0,0,0,230,231,5,
        45,0,0,231,232,5,42,0,0,232,233,3,36,18,0,233,35,1,0,0,0,234,236,
        5,12,0,0,235,237,3,38,19,0,236,235,1,0,0,0,236,237,1,0,0,0,237,238,
        1,0,0,0,238,245,5,14,0,0,239,241,5,2,0,0,240,242,3,38,19,0,241,240,
        1,0,0,0,241,242,1,0,0,0,242,243,1,0,0,0,243,245,5,3,0,0,244,234,
        1,0,0,0,244,239,1,0,0,0,245,37,1,0,0,0,246,249,3,28,14,0,247,248,
        5,13,0,0,248,250,3,28,14,0,249,247,1,0,0,0,249,250,1,0,0,0,250,39,
        1,0,0,0,251,256,5,46,0,0,252,256,5,44,0,0,253,256,3,42,21,0,254,
        256,3,44,22,0,255,251,1,0,0,0,255,252,1,0,0,0,255,253,1,0,0,0,255,
        254,1,0,0,0,256,41,1,0,0,0,257,258,5,12,0,0,258,263,3,28,14,0,259,
        260,5,5,0,0,260,262,3,28,14,0,261,259,1,0,0,0,262,265,1,0,0,0,263,
        261,1,0,0,0,263,264,1,0,0,0,264,266,1,0,0,0,265,263,1,0,0,0,266,
        267,5,14,0,0,267,43,1,0,0,0,268,272,5,43,0,0,269,271,9,0,0,0,270,
        269,1,0,0,0,271,274,1,0,0,0,272,273,1,0,0,0,272,270,1,0,0,0,273,
        275,1,0,0,0,274,272,1,0,0,0,275,276,5,43,0,0,276,45,1,0,0,0,28,49,
        55,59,62,71,99,105,109,118,122,127,149,159,170,173,200,203,205,213,
        220,227,236,241,244,249,255,263,272
    ]

class RustParser ( Parser ):

    grammarFileName = "Rust.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'fn'", "'('", "')'", "'->'", "','", "':'", 
                     "'&'", "'i32'", "'Vec'", "'<'", "'>'", "'['", "';'", 
                     "']'", "'{'", "'}'", "'let'", "'mut'", "'='", "'for'", 
                     "'in'", "'if'", "'else'", "'return'", "'.'", "'*'", 
                     "'/'", "'%'", "'+'", "'-'", "'>>'", "'=='", "'..'", 
                     "'+='", "'-='", "'*='", "'/='", "'%='", "'&='", "'|='", 
                     "'^='", "'!'", "'\"'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "Binary", "Identifier", "Number", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_functionDef = 1
    RULE_paramList = 2
    RULE_param = 3
    RULE_referenceType = 4
    RULE_type = 5
    RULE_block = 6
    RULE_statement = 7
    RULE_letStmt = 8
    RULE_assignStmt = 9
    RULE_forStmt = 10
    RULE_ifStmt = 11
    RULE_exprStmt = 12
    RULE_returnStmt = 13
    RULE_expression = 14
    RULE_primaryExpression = 15
    RULE_argumentList = 16
    RULE_macroCall = 17
    RULE_macroArgs = 18
    RULE_macroInner = 19
    RULE_literal = 20
    RULE_arrayLiteral = 21
    RULE_stringLiteral = 22

    ruleNames =  [ "program", "functionDef", "paramList", "param", "referenceType", 
                   "type", "block", "statement", "letStmt", "assignStmt", 
                   "forStmt", "ifStmt", "exprStmt", "returnStmt", "expression", 
                   "primaryExpression", "argumentList", "macroCall", "macroArgs", 
                   "macroInner", "literal", "arrayLiteral", "stringLiteral" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    Binary=44
    Identifier=45
    Number=46
    WS=47
    COMMENT=48

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.FunctionDefContext)
            else:
                return self.getTypedRuleContext(RustParser.FunctionDefContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = RustParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 46
                self.functionDef()
                self.state = 49 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def block(self):
            return self.getTypedRuleContext(RustParser.BlockContext,0)


        def paramList(self):
            return self.getTypedRuleContext(RustParser.ParamListContext,0)


        def type_(self):
            return self.getTypedRuleContext(RustParser.TypeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_functionDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDef" ):
                listener.enterFunctionDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDef" ):
                listener.exitFunctionDef(self)




    def functionDef(self):

        localctx = RustParser.FunctionDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_functionDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(RustParser.T__0)
            self.state = 52
            self.match(RustParser.Identifier)
            self.state = 53
            self.match(RustParser.T__1)
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 54
                self.paramList()


            self.state = 57
            self.match(RustParser.T__2)
            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 58
                self.match(RustParser.T__3)


            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 4992) != 0):
                self.state = 61
                self.type_()


            self.state = 64
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ParamContext)
            else:
                return self.getTypedRuleContext(RustParser.ParamContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)




    def paramList(self):

        localctx = RustParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.param()
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 67
                self.match(RustParser.T__4)
                self.state = 68
                self.param()
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def referenceType(self):
            return self.getTypedRuleContext(RustParser.ReferenceTypeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)




    def param(self):

        localctx = RustParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(RustParser.Identifier)
            self.state = 75
            self.match(RustParser.T__5)
            self.state = 76
            self.referenceType()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReferenceTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(RustParser.TypeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_referenceType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReferenceType" ):
                listener.enterReferenceType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReferenceType" ):
                listener.exitReferenceType(self)




    def referenceType(self):

        localctx = RustParser.ReferenceTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_referenceType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self.match(RustParser.T__6)
            self.state = 79
            self.type_()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(RustParser.TypeContext,0)


        def Number(self):
            return self.getToken(RustParser.Number, 0)

        def getRuleIndex(self):
            return RustParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)




    def type_(self):

        localctx = RustParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_type)
        try:
            self.state = 99
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 81
                self.match(RustParser.T__7)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 82
                self.match(RustParser.T__8)
                self.state = 83
                self.match(RustParser.T__9)
                self.state = 84
                self.type_()
                self.state = 85
                self.match(RustParser.T__10)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 87
                self.match(RustParser.T__6)
                self.state = 88
                self.type_()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 89
                self.match(RustParser.T__11)
                self.state = 90
                self.type_()
                self.state = 91
                self.match(RustParser.T__12)
                self.state = 92
                self.match(RustParser.Number)
                self.state = 93
                self.match(RustParser.T__13)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 95
                self.match(RustParser.T__11)
                self.state = 96
                self.type_()
                self.state = 97
                self.match(RustParser.T__13)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.StatementContext)
            else:
                return self.getTypedRuleContext(RustParser.StatementContext,i)


        def returnStmt(self):
            return self.getTypedRuleContext(RustParser.ReturnStmtContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)




    def block(self):

        localctx = RustParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self.match(RustParser.T__14)
            self.state = 105
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 102
                    self.statement() 
                self.state = 107
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 109
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 131941412114564) != 0):
                self.state = 108
                self.returnStmt()


            self.state = 111
            self.match(RustParser.T__15)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def letStmt(self):
            return self.getTypedRuleContext(RustParser.LetStmtContext,0)


        def assignStmt(self):
            return self.getTypedRuleContext(RustParser.AssignStmtContext,0)


        def forStmt(self):
            return self.getTypedRuleContext(RustParser.ForStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(RustParser.IfStmtContext,0)


        def exprStmt(self):
            return self.getTypedRuleContext(RustParser.ExprStmtContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = RustParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_statement)
        try:
            self.state = 118
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 113
                self.letStmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 114
                self.assignStmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 115
                self.forStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 116
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 117
                self.exprStmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def type_(self):
            return self.getTypedRuleContext(RustParser.TypeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_letStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetStmt" ):
                listener.enterLetStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetStmt" ):
                listener.exitLetStmt(self)




    def letStmt(self):

        localctx = RustParser.LetStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_letStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(RustParser.T__16)
            self.state = 122
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==18:
                self.state = 121
                self.match(RustParser.T__17)


            self.state = 124
            self.match(RustParser.Identifier)
            self.state = 127
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 125
                self.match(RustParser.T__5)
                self.state = 126
                self.type_()


            self.state = 129
            self.match(RustParser.T__18)
            self.state = 130
            self.expression(0)
            self.state = 131
            self.match(RustParser.T__12)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RustParser.ExpressionContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_assignStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignStmt" ):
                listener.enterAssignStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignStmt" ):
                listener.exitAssignStmt(self)




    def assignStmt(self):

        localctx = RustParser.AssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_assignStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self.expression(0)
            self.state = 134
            self.match(RustParser.T__18)
            self.state = 135
            self.expression(0)
            self.state = 136
            self.match(RustParser.T__12)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def block(self):
            return self.getTypedRuleContext(RustParser.BlockContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_forStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStmt" ):
                listener.enterForStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStmt" ):
                listener.exitForStmt(self)




    def forStmt(self):

        localctx = RustParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_forStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(RustParser.T__19)
            self.state = 139
            self.match(RustParser.Identifier)
            self.state = 140
            self.match(RustParser.T__20)
            self.state = 141
            self.expression(0)
            self.state = 142
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.BlockContext)
            else:
                return self.getTypedRuleContext(RustParser.BlockContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)




    def ifStmt(self):

        localctx = RustParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self.match(RustParser.T__21)
            self.state = 145
            self.expression(0)
            self.state = 146
            self.block()
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==23:
                self.state = 147
                self.match(RustParser.T__22)
                self.state = 148
                self.block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_exprStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprStmt" ):
                listener.enterExprStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprStmt" ):
                listener.exitExprStmt(self)




    def exprStmt(self):

        localctx = RustParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_exprStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.expression(0)
            self.state = 152
            self.match(RustParser.T__12)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)




    def returnStmt(self):

        localctx = RustParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_returnStmt)
        try:
            self.state = 159
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [24]:
                self.enterOuterAlt(localctx, 1)
                self.state = 154
                self.match(RustParser.T__23)
                self.state = 155
                self.expression(0)
                self.state = 156
                self.match(RustParser.T__12)
                pass
            elif token in [2, 7, 12, 43, 44, 45, 46]:
                self.enterOuterAlt(localctx, 2)
                self.state = 158
                self.expression(0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primaryExpression(self):
            return self.getTypedRuleContext(RustParser.PrimaryExpressionContext,0)


        def macroCall(self):
            return self.getTypedRuleContext(RustParser.MacroCallContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RustParser.ExpressionContext,i)


        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def argumentList(self):
            return self.getTypedRuleContext(RustParser.ArgumentListContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RustParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 28
        self.enterRecursionRule(localctx, 28, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 173
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.state = 162
                self.primaryExpression()
                pass

            elif la_ == 2:
                self.state = 163
                self.macroCall()
                pass

            elif la_ == 3:
                self.state = 164
                self.match(RustParser.T__6)
                self.state = 165
                self.expression(9)
                pass

            elif la_ == 4:
                self.state = 166
                self.match(RustParser.Identifier)
                self.state = 167
                self.match(RustParser.T__41)
                self.state = 168
                self.match(RustParser.T__1)
                self.state = 170
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 131941395337348) != 0):
                    self.state = 169
                    self.argumentList()


                self.state = 172
                self.match(RustParser.T__2)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 205
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 203
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
                    if la_ == 1:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 175
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 176
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4227858560) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 177
                        self.expression(6)
                        pass

                    elif la_ == 2:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 178
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 179
                        self.match(RustParser.T__31)
                        self.state = 180
                        self.expression(5)
                        pass

                    elif la_ == 3:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 181
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 182
                        self.match(RustParser.T__32)
                        self.state = 183
                        self.expression(4)
                        pass

                    elif la_ == 4:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 184
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 185
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4380866641920) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 186
                        self.expression(3)
                        pass

                    elif la_ == 5:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 187
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 188
                        self.match(RustParser.T__11)
                        self.state = 189
                        self.expression(0)
                        self.state = 190
                        self.match(RustParser.T__13)
                        pass

                    elif la_ == 6:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 192
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 193
                        self.match(RustParser.T__24)
                        self.state = 194
                        self.match(RustParser.Identifier)
                        pass

                    elif la_ == 7:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 195
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 196
                        self.match(RustParser.T__24)
                        self.state = 197
                        self.match(RustParser.Identifier)
                        self.state = 198
                        self.match(RustParser.T__1)
                        self.state = 200
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 131941395337348) != 0):
                            self.state = 199
                            self.argumentList()


                        self.state = 202
                        self.match(RustParser.T__2)
                        pass

             
                self.state = 207
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PrimaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(RustParser.LiteralContext,0)


        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def argumentList(self):
            return self.getTypedRuleContext(RustParser.ArgumentListContext,0)


        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_primaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryExpression" ):
                listener.enterPrimaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryExpression" ):
                listener.exitPrimaryExpression(self)




    def primaryExpression(self):

        localctx = RustParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_primaryExpression)
        self._la = 0 # Token type
        try:
            self.state = 220
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 208
                self.literal()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 209
                self.match(RustParser.Identifier)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 210
                self.match(RustParser.Identifier)
                self.state = 211
                self.match(RustParser.T__1)
                self.state = 213
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 131941395337348) != 0):
                    self.state = 212
                    self.argumentList()


                self.state = 215
                self.match(RustParser.T__2)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 216
                self.match(RustParser.T__1)
                self.state = 217
                self.expression(0)
                self.state = 218
                self.match(RustParser.T__2)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RustParser.ExpressionContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_argumentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgumentList" ):
                listener.enterArgumentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgumentList" ):
                listener.exitArgumentList(self)




    def argumentList(self):

        localctx = RustParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            self.expression(0)
            self.state = 227
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 223
                self.match(RustParser.T__4)
                self.state = 224
                self.expression(0)
                self.state = 229
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MacroCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def macroArgs(self):
            return self.getTypedRuleContext(RustParser.MacroArgsContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_macroCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacroCall" ):
                listener.enterMacroCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacroCall" ):
                listener.exitMacroCall(self)




    def macroCall(self):

        localctx = RustParser.MacroCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_macroCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            self.match(RustParser.Identifier)
            self.state = 231
            self.match(RustParser.T__41)
            self.state = 232
            self.macroArgs()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MacroArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def macroInner(self):
            return self.getTypedRuleContext(RustParser.MacroInnerContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_macroArgs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacroArgs" ):
                listener.enterMacroArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacroArgs" ):
                listener.exitMacroArgs(self)




    def macroArgs(self):

        localctx = RustParser.MacroArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_macroArgs)
        self._la = 0 # Token type
        try:
            self.state = 244
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 234
                self.match(RustParser.T__11)
                self.state = 236
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 131941395337348) != 0):
                    self.state = 235
                    self.macroInner()


                self.state = 238
                self.match(RustParser.T__13)
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 239
                self.match(RustParser.T__1)
                self.state = 241
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 131941395337348) != 0):
                    self.state = 240
                    self.macroInner()


                self.state = 243
                self.match(RustParser.T__2)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MacroInnerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RustParser.ExpressionContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_macroInner

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacroInner" ):
                listener.enterMacroInner(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacroInner" ):
                listener.exitMacroInner(self)




    def macroInner(self):

        localctx = RustParser.MacroInnerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_macroInner)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 246
            self.expression(0)
            self.state = 249
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 247
                self.match(RustParser.T__12)
                self.state = 248
                self.expression(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self):
            return self.getToken(RustParser.Number, 0)

        def Binary(self):
            return self.getToken(RustParser.Binary, 0)

        def arrayLiteral(self):
            return self.getTypedRuleContext(RustParser.ArrayLiteralContext,0)


        def stringLiteral(self):
            return self.getTypedRuleContext(RustParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)




    def literal(self):

        localctx = RustParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_literal)
        try:
            self.state = 255
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [46]:
                self.enterOuterAlt(localctx, 1)
                self.state = 251
                self.match(RustParser.Number)
                pass
            elif token in [44]:
                self.enterOuterAlt(localctx, 2)
                self.state = 252
                self.match(RustParser.Binary)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 3)
                self.state = 253
                self.arrayLiteral()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 4)
                self.state = 254
                self.stringLiteral()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RustParser.ExpressionContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_arrayLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayLiteral" ):
                listener.enterArrayLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayLiteral" ):
                listener.exitArrayLiteral(self)




    def arrayLiteral(self):

        localctx = RustParser.ArrayLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_arrayLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self.match(RustParser.T__11)
            self.state = 258
            self.expression(0)
            self.state = 263
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 259
                self.match(RustParser.T__4)
                self.state = 260
                self.expression(0)
                self.state = 265
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 266
            self.match(RustParser.T__13)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return RustParser.RULE_stringLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteral" ):
                listener.enterStringLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteral" ):
                listener.exitStringLiteral(self)




    def stringLiteral(self):

        localctx = RustParser.StringLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_stringLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 268
            self.match(RustParser.T__42)
            self.state = 272
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,27,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 269
                    self.matchWildcard() 
                self.state = 274
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,27,self._ctx)

            self.state = 275
            self.match(RustParser.T__42)
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
        self._predicates[14] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 6)
         




