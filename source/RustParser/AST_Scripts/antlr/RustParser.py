# Generated from Rust.g4 by ANTLR 4.13.2
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
        4,1,53,370,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,1,0,5,0,70,8,0,10,0,12,0,73,9,0,1,1,1,1,1,1,3,1,78,8,1,1,2,
        1,2,1,2,1,2,5,2,84,8,2,10,2,12,2,87,9,2,1,2,1,2,1,3,1,3,1,3,1,3,
        3,3,95,8,3,1,4,1,4,1,4,1,4,3,4,101,8,4,1,4,1,4,3,4,105,8,4,1,4,3,
        4,108,8,4,1,4,1,4,1,5,1,5,1,5,5,5,115,8,5,10,5,12,5,118,9,5,1,6,
        1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,
        5,9,137,8,9,10,9,12,9,140,9,9,1,9,1,9,3,9,144,8,9,1,9,1,9,1,9,1,
        9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,3,9,158,8,9,1,10,1,10,5,10,162,
        8,10,10,10,12,10,165,9,10,1,10,3,10,168,8,10,1,10,1,10,1,11,1,11,
        1,11,1,11,1,11,3,11,177,8,11,1,12,1,12,1,12,1,12,1,12,1,12,1,13,
        1,13,3,13,187,8,13,1,14,1,14,1,14,3,14,192,8,14,1,15,1,15,1,15,1,
        15,3,15,198,8,15,1,16,1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,17,1,
        17,1,17,1,18,1,18,1,18,1,18,1,18,3,18,216,8,18,1,19,1,19,1,19,1,
        20,1,20,1,20,1,20,1,20,3,20,226,8,20,1,21,1,21,1,21,1,21,1,21,1,
        21,1,21,1,21,1,21,3,21,237,8,21,1,21,3,21,240,8,21,1,21,1,21,1,21,
        1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,
        1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,3,21,267,8,21,1,21,
        5,21,270,8,21,10,21,12,21,273,9,21,1,22,1,22,1,22,1,23,1,23,1,23,
        1,23,1,23,3,23,283,8,23,1,23,1,23,1,23,1,23,1,23,3,23,290,8,23,1,
        24,1,24,1,24,5,24,295,8,24,10,24,12,24,298,9,24,1,25,1,25,1,25,1,
        25,1,26,1,26,3,26,306,8,26,1,26,1,26,1,26,3,26,311,8,26,1,26,3,26,
        314,8,26,1,27,1,27,1,27,3,27,319,8,27,1,28,1,28,1,28,1,28,1,28,1,
        29,1,29,1,29,1,29,1,29,5,29,331,8,29,10,29,12,29,334,9,29,3,29,336,
        8,29,1,29,3,29,339,8,29,1,30,1,30,1,30,1,30,1,30,3,30,346,8,30,1,
        31,1,31,1,32,1,32,1,32,1,32,5,32,354,8,32,10,32,12,32,357,9,32,1,
        32,1,32,1,33,1,33,5,33,363,8,33,10,33,12,33,366,9,33,1,33,1,33,1,
        33,1,364,1,42,34,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,
        36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,0,3,2,0,9,9,24,29,
        1,0,32,39,1,0,42,43,394,0,71,1,0,0,0,2,77,1,0,0,0,4,79,1,0,0,0,6,
        90,1,0,0,0,8,96,1,0,0,0,10,111,1,0,0,0,12,119,1,0,0,0,14,123,1,0,
        0,0,16,126,1,0,0,0,18,157,1,0,0,0,20,159,1,0,0,0,22,176,1,0,0,0,
        24,178,1,0,0,0,26,186,1,0,0,0,28,188,1,0,0,0,30,193,1,0,0,0,32,199,
        1,0,0,0,34,204,1,0,0,0,36,210,1,0,0,0,38,217,1,0,0,0,40,225,1,0,
        0,0,42,239,1,0,0,0,44,274,1,0,0,0,46,289,1,0,0,0,48,291,1,0,0,0,
        50,299,1,0,0,0,52,313,1,0,0,0,54,315,1,0,0,0,56,320,1,0,0,0,58,325,
        1,0,0,0,60,345,1,0,0,0,62,347,1,0,0,0,64,349,1,0,0,0,66,360,1,0,
        0,0,68,70,3,2,1,0,69,68,1,0,0,0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,
        1,0,0,0,72,1,1,0,0,0,73,71,1,0,0,0,74,78,3,8,4,0,75,78,3,4,2,0,76,
        78,3,56,28,0,77,74,1,0,0,0,77,75,1,0,0,0,77,76,1,0,0,0,78,3,1,0,
        0,0,79,80,5,1,0,0,80,81,5,45,0,0,81,85,5,2,0,0,82,84,3,6,3,0,83,
        82,1,0,0,0,84,87,1,0,0,0,85,83,1,0,0,0,85,86,1,0,0,0,86,88,1,0,0,
        0,87,85,1,0,0,0,88,89,5,3,0,0,89,5,1,0,0,0,90,91,5,45,0,0,91,92,
        5,4,0,0,92,94,3,16,8,0,93,95,5,51,0,0,94,93,1,0,0,0,94,95,1,0,0,
        0,95,7,1,0,0,0,96,97,5,5,0,0,97,98,5,45,0,0,98,100,5,6,0,0,99,101,
        3,10,5,0,100,99,1,0,0,0,100,101,1,0,0,0,101,102,1,0,0,0,102,104,
        5,7,0,0,103,105,5,8,0,0,104,103,1,0,0,0,104,105,1,0,0,0,105,107,
        1,0,0,0,106,108,3,16,8,0,107,106,1,0,0,0,107,108,1,0,0,0,108,109,
        1,0,0,0,109,110,3,20,10,0,110,9,1,0,0,0,111,116,3,12,6,0,112,113,
        5,51,0,0,113,115,3,12,6,0,114,112,1,0,0,0,115,118,1,0,0,0,116,114,
        1,0,0,0,116,117,1,0,0,0,117,11,1,0,0,0,118,116,1,0,0,0,119,120,5,
        45,0,0,120,121,5,4,0,0,121,122,3,14,7,0,122,13,1,0,0,0,123,124,5,
        9,0,0,124,125,3,16,8,0,125,15,1,0,0,0,126,127,3,18,9,0,127,17,1,
        0,0,0,128,158,5,10,0,0,129,158,5,11,0,0,130,158,5,12,0,0,131,143,
        5,45,0,0,132,133,5,13,0,0,133,138,3,16,8,0,134,135,5,51,0,0,135,
        137,3,16,8,0,136,134,1,0,0,0,137,140,1,0,0,0,138,136,1,0,0,0,138,
        139,1,0,0,0,139,141,1,0,0,0,140,138,1,0,0,0,141,142,5,47,0,0,142,
        144,1,0,0,0,143,132,1,0,0,0,143,144,1,0,0,0,144,158,1,0,0,0,145,
        146,5,9,0,0,146,158,3,16,8,0,147,148,5,49,0,0,148,149,3,16,8,0,149,
        150,5,14,0,0,150,151,5,46,0,0,151,152,5,50,0,0,152,158,1,0,0,0,153,
        154,5,49,0,0,154,155,3,16,8,0,155,156,5,50,0,0,156,158,1,0,0,0,157,
        128,1,0,0,0,157,129,1,0,0,0,157,130,1,0,0,0,157,131,1,0,0,0,157,
        145,1,0,0,0,157,147,1,0,0,0,157,153,1,0,0,0,158,19,1,0,0,0,159,163,
        5,2,0,0,160,162,3,22,11,0,161,160,1,0,0,0,162,165,1,0,0,0,163,161,
        1,0,0,0,163,164,1,0,0,0,164,167,1,0,0,0,165,163,1,0,0,0,166,168,
        3,40,20,0,167,166,1,0,0,0,167,168,1,0,0,0,168,169,1,0,0,0,169,170,
        5,3,0,0,170,21,1,0,0,0,171,177,3,24,12,0,172,177,3,32,16,0,173,177,
        3,34,17,0,174,177,3,36,18,0,175,177,3,38,19,0,176,171,1,0,0,0,176,
        172,1,0,0,0,176,173,1,0,0,0,176,174,1,0,0,0,176,175,1,0,0,0,177,
        23,1,0,0,0,178,179,5,15,0,0,179,180,3,26,13,0,180,181,5,16,0,0,181,
        182,3,42,21,0,182,183,5,14,0,0,183,25,1,0,0,0,184,187,3,30,15,0,
        185,187,3,28,14,0,186,184,1,0,0,0,186,185,1,0,0,0,187,27,1,0,0,0,
        188,191,5,45,0,0,189,190,5,4,0,0,190,192,3,16,8,0,191,189,1,0,0,
        0,191,192,1,0,0,0,192,29,1,0,0,0,193,194,5,17,0,0,194,197,5,45,0,
        0,195,196,5,4,0,0,196,198,3,16,8,0,197,195,1,0,0,0,197,198,1,0,0,
        0,198,31,1,0,0,0,199,200,3,42,21,0,200,201,5,16,0,0,201,202,3,42,
        21,0,202,203,5,14,0,0,203,33,1,0,0,0,204,205,5,18,0,0,205,206,5,
        45,0,0,206,207,5,19,0,0,207,208,3,42,21,0,208,209,3,20,10,0,209,
        35,1,0,0,0,210,211,5,20,0,0,211,212,3,42,21,0,212,215,3,20,10,0,
        213,214,5,21,0,0,214,216,3,20,10,0,215,213,1,0,0,0,215,216,1,0,0,
        0,216,37,1,0,0,0,217,218,3,42,21,0,218,219,5,14,0,0,219,39,1,0,0,
        0,220,221,5,22,0,0,221,222,3,42,21,0,222,223,5,14,0,0,223,226,1,
        0,0,0,224,226,3,42,21,0,225,220,1,0,0,0,225,224,1,0,0,0,226,41,1,
        0,0,0,227,228,6,21,-1,0,228,240,3,60,30,0,229,240,3,46,23,0,230,
        240,3,50,25,0,231,240,3,44,22,0,232,233,5,45,0,0,233,234,5,40,0,
        0,234,236,5,6,0,0,235,237,3,48,24,0,236,235,1,0,0,0,236,237,1,0,
        0,0,237,238,1,0,0,0,238,240,5,7,0,0,239,227,1,0,0,0,239,229,1,0,
        0,0,239,230,1,0,0,0,239,231,1,0,0,0,239,232,1,0,0,0,240,271,1,0,
        0,0,241,242,10,5,0,0,242,243,7,0,0,0,243,270,3,42,21,6,244,245,10,
        4,0,0,245,246,5,30,0,0,246,270,3,42,21,5,247,248,10,3,0,0,248,249,
        5,31,0,0,249,270,3,42,21,4,250,251,10,2,0,0,251,252,7,1,0,0,252,
        270,3,42,21,3,253,254,10,8,0,0,254,255,5,49,0,0,255,256,3,42,21,
        0,256,257,5,50,0,0,257,270,1,0,0,0,258,259,10,7,0,0,259,260,5,23,
        0,0,260,270,5,45,0,0,261,262,10,6,0,0,262,263,5,23,0,0,263,264,5,
        45,0,0,264,266,5,6,0,0,265,267,3,48,24,0,266,265,1,0,0,0,266,267,
        1,0,0,0,267,268,1,0,0,0,268,270,5,7,0,0,269,241,1,0,0,0,269,244,
        1,0,0,0,269,247,1,0,0,0,269,250,1,0,0,0,269,253,1,0,0,0,269,258,
        1,0,0,0,269,261,1,0,0,0,270,273,1,0,0,0,271,269,1,0,0,0,271,272,
        1,0,0,0,272,43,1,0,0,0,273,271,1,0,0,0,274,275,5,9,0,0,275,276,3,
        42,21,0,276,45,1,0,0,0,277,290,3,60,30,0,278,290,5,45,0,0,279,280,
        5,45,0,0,280,282,5,6,0,0,281,283,3,48,24,0,282,281,1,0,0,0,282,283,
        1,0,0,0,283,284,1,0,0,0,284,290,5,7,0,0,285,286,5,6,0,0,286,287,
        3,42,21,0,287,288,5,7,0,0,288,290,1,0,0,0,289,277,1,0,0,0,289,278,
        1,0,0,0,289,279,1,0,0,0,289,285,1,0,0,0,290,47,1,0,0,0,291,296,3,
        42,21,0,292,293,5,51,0,0,293,295,3,42,21,0,294,292,1,0,0,0,295,298,
        1,0,0,0,296,294,1,0,0,0,296,297,1,0,0,0,297,49,1,0,0,0,298,296,1,
        0,0,0,299,300,5,45,0,0,300,301,5,40,0,0,301,302,3,52,26,0,302,51,
        1,0,0,0,303,305,5,49,0,0,304,306,3,54,27,0,305,304,1,0,0,0,305,306,
        1,0,0,0,306,307,1,0,0,0,307,314,5,50,0,0,308,310,5,6,0,0,309,311,
        3,54,27,0,310,309,1,0,0,0,310,311,1,0,0,0,311,312,1,0,0,0,312,314,
        5,7,0,0,313,303,1,0,0,0,313,308,1,0,0,0,314,53,1,0,0,0,315,318,3,
        42,21,0,316,317,5,14,0,0,317,319,3,42,21,0,318,316,1,0,0,0,318,319,
        1,0,0,0,319,55,1,0,0,0,320,321,5,48,0,0,321,322,5,49,0,0,322,323,
        3,58,29,0,323,324,5,50,0,0,324,57,1,0,0,0,325,338,5,45,0,0,326,335,
        5,6,0,0,327,332,5,45,0,0,328,329,5,51,0,0,329,331,5,45,0,0,330,328,
        1,0,0,0,331,334,1,0,0,0,332,330,1,0,0,0,332,333,1,0,0,0,333,336,
        1,0,0,0,334,332,1,0,0,0,335,327,1,0,0,0,335,336,1,0,0,0,336,337,
        1,0,0,0,337,339,5,7,0,0,338,326,1,0,0,0,338,339,1,0,0,0,339,59,1,
        0,0,0,340,346,3,64,32,0,341,346,5,46,0,0,342,346,5,44,0,0,343,346,
        3,66,33,0,344,346,3,62,31,0,345,340,1,0,0,0,345,341,1,0,0,0,345,
        342,1,0,0,0,345,343,1,0,0,0,345,344,1,0,0,0,346,61,1,0,0,0,347,348,
        7,2,0,0,348,63,1,0,0,0,349,350,5,49,0,0,350,355,3,42,21,0,351,352,
        5,51,0,0,352,354,3,42,21,0,353,351,1,0,0,0,354,357,1,0,0,0,355,353,
        1,0,0,0,355,356,1,0,0,0,356,358,1,0,0,0,357,355,1,0,0,0,358,359,
        5,50,0,0,359,65,1,0,0,0,360,364,5,41,0,0,361,363,9,0,0,0,362,361,
        1,0,0,0,363,366,1,0,0,0,364,365,1,0,0,0,364,362,1,0,0,0,365,367,
        1,0,0,0,366,364,1,0,0,0,367,368,5,41,0,0,368,67,1,0,0,0,37,71,77,
        85,94,100,104,107,116,138,143,157,163,167,176,186,191,197,215,225,
        236,239,266,269,271,282,289,296,305,310,313,318,332,335,338,345,
        355,364
    ]

class RustParser ( Parser ):

    grammarFileName = "Rust.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'struct'", "'{'", "'}'", "':'", "'fn'", 
                     "'('", "')'", "'->'", "'&'", "'i32'", "'String'", "'bool'", 
                     "'<'", "';'", "'let'", "'='", "'mut'", "'for'", "'in'", 
                     "'if'", "'else'", "'return'", "'.'", "'*'", "'/'", 
                     "'%'", "'+'", "'-'", "'>>'", "'=='", "'..'", "'+='", 
                     "'-='", "'*='", "'/='", "'%='", "'&='", "'|='", "'^='", 
                     "'!'", "'\"'", "'true'", "'false'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'>'", "'#'", "'['", "']'", "','" ]

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
                      "<INVALID>", "<INVALID>", "TRUE", "FALSE", "Binary", 
                      "Identifier", "Number", "GT", "POUND", "LBRACK", "RBRACK", 
                      "COMMA", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_topLevelItem = 1
    RULE_structDef = 2
    RULE_structField = 3
    RULE_functionDef = 4
    RULE_paramList = 5
    RULE_param = 6
    RULE_referenceType = 7
    RULE_type = 8
    RULE_basicType = 9
    RULE_block = 10
    RULE_statement = 11
    RULE_letStmt = 12
    RULE_varDef = 13
    RULE_immutableDef = 14
    RULE_mutableDef = 15
    RULE_assignStmt = 16
    RULE_forStmt = 17
    RULE_ifStmt = 18
    RULE_exprStmt = 19
    RULE_returnStmt = 20
    RULE_expression = 21
    RULE_borrowExpression = 22
    RULE_primaryExpression = 23
    RULE_argumentList = 24
    RULE_macroCall = 25
    RULE_macroArgs = 26
    RULE_macroInner = 27
    RULE_attribute = 28
    RULE_attrInner = 29
    RULE_literal = 30
    RULE_booleanLiteral = 31
    RULE_arrayLiteral = 32
    RULE_stringLiteral = 33

    ruleNames =  [ "program", "topLevelItem", "structDef", "structField", 
                   "functionDef", "paramList", "param", "referenceType", 
                   "type", "basicType", "block", "statement", "letStmt", 
                   "varDef", "immutableDef", "mutableDef", "assignStmt", 
                   "forStmt", "ifStmt", "exprStmt", "returnStmt", "expression", 
                   "borrowExpression", "primaryExpression", "argumentList", 
                   "macroCall", "macroArgs", "macroInner", "attribute", 
                   "attrInner", "literal", "booleanLiteral", "arrayLiteral", 
                   "stringLiteral" ]

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
    TRUE=42
    FALSE=43
    Binary=44
    Identifier=45
    Number=46
    GT=47
    POUND=48
    LBRACK=49
    RBRACK=50
    COMMA=51
    WS=52
    COMMENT=53

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def topLevelItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.TopLevelItemContext)
            else:
                return self.getTypedRuleContext(RustParser.TopLevelItemContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = RustParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 281474976710690) != 0):
                self.state = 68
                self.topLevelItem()
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


    class TopLevelItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionDef(self):
            return self.getTypedRuleContext(RustParser.FunctionDefContext,0)


        def structDef(self):
            return self.getTypedRuleContext(RustParser.StructDefContext,0)


        def attribute(self):
            return self.getTypedRuleContext(RustParser.AttributeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_topLevelItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTopLevelItem" ):
                listener.enterTopLevelItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTopLevelItem" ):
                listener.exitTopLevelItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTopLevelItem" ):
                return visitor.visitTopLevelItem(self)
            else:
                return visitor.visitChildren(self)




    def topLevelItem(self):

        localctx = RustParser.TopLevelItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_topLevelItem)
        try:
            self.state = 77
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 74
                self.functionDef()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 75
                self.structDef()
                pass
            elif token in [48]:
                self.enterOuterAlt(localctx, 3)
                self.state = 76
                self.attribute()
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


    class StructDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def structField(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.StructFieldContext)
            else:
                return self.getTypedRuleContext(RustParser.StructFieldContext,i)


        def getRuleIndex(self):
            return RustParser.RULE_structDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStructDef" ):
                listener.enterStructDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStructDef" ):
                listener.exitStructDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStructDef" ):
                return visitor.visitStructDef(self)
            else:
                return visitor.visitChildren(self)




    def structDef(self):

        localctx = RustParser.StructDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_structDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(RustParser.T__0)
            self.state = 80
            self.match(RustParser.Identifier)
            self.state = 81
            self.match(RustParser.T__1)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 82
                self.structField()
                self.state = 87
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 88
            self.match(RustParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StructFieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def type_(self):
            return self.getTypedRuleContext(RustParser.TypeContext,0)


        def COMMA(self):
            return self.getToken(RustParser.COMMA, 0)

        def getRuleIndex(self):
            return RustParser.RULE_structField

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStructField" ):
                listener.enterStructField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStructField" ):
                listener.exitStructField(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStructField" ):
                return visitor.visitStructField(self)
            else:
                return visitor.visitChildren(self)




    def structField(self):

        localctx = RustParser.StructFieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_structField)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(RustParser.Identifier)
            self.state = 91
            self.match(RustParser.T__3)
            self.state = 92
            self.type_()
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==51:
                self.state = 93
                self.match(RustParser.COMMA)


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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDef" ):
                return visitor.visitFunctionDef(self)
            else:
                return visitor.visitChildren(self)




    def functionDef(self):

        localctx = RustParser.FunctionDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_functionDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.match(RustParser.T__4)
            self.state = 97
            self.match(RustParser.Identifier)
            self.state = 98
            self.match(RustParser.T__5)
            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 99
                self.paramList()


            self.state = 102
            self.match(RustParser.T__6)
            self.state = 104
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 103
                self.match(RustParser.T__7)


            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 598134325517824) != 0):
                self.state = 106
                self.type_()


            self.state = 109
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


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RustParser.COMMA)
            else:
                return self.getToken(RustParser.COMMA, i)

        def getRuleIndex(self):
            return RustParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = RustParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self.param()
            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==51:
                self.state = 112
                self.match(RustParser.COMMA)
                self.state = 113
                self.param()
                self.state = 118
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = RustParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.match(RustParser.Identifier)
            self.state = 120
            self.match(RustParser.T__3)
            self.state = 121
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReferenceType" ):
                return visitor.visitReferenceType(self)
            else:
                return visitor.visitChildren(self)




    def referenceType(self):

        localctx = RustParser.ReferenceTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_referenceType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(RustParser.T__8)
            self.state = 124
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

        def basicType(self):
            return self.getTypedRuleContext(RustParser.BasicTypeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = RustParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self.basicType()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BasicTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.TypeContext)
            else:
                return self.getTypedRuleContext(RustParser.TypeContext,i)


        def GT(self):
            return self.getToken(RustParser.GT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RustParser.COMMA)
            else:
                return self.getToken(RustParser.COMMA, i)

        def LBRACK(self):
            return self.getToken(RustParser.LBRACK, 0)

        def Number(self):
            return self.getToken(RustParser.Number, 0)

        def RBRACK(self):
            return self.getToken(RustParser.RBRACK, 0)

        def getRuleIndex(self):
            return RustParser.RULE_basicType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBasicType" ):
                listener.enterBasicType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBasicType" ):
                listener.exitBasicType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBasicType" ):
                return visitor.visitBasicType(self)
            else:
                return visitor.visitChildren(self)




    def basicType(self):

        localctx = RustParser.BasicTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_basicType)
        self._la = 0 # Token type
        try:
            self.state = 157
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 128
                self.match(RustParser.T__9)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 129
                self.match(RustParser.T__10)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 130
                self.match(RustParser.T__11)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 131
                self.match(RustParser.Identifier)
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==13:
                    self.state = 132
                    self.match(RustParser.T__12)
                    self.state = 133
                    self.type_()
                    self.state = 138
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==51:
                        self.state = 134
                        self.match(RustParser.COMMA)
                        self.state = 135
                        self.type_()
                        self.state = 140
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 141
                    self.match(RustParser.GT)


                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 145
                self.match(RustParser.T__8)
                self.state = 146
                self.type_()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 147
                self.match(RustParser.LBRACK)
                self.state = 148
                self.type_()
                self.state = 149
                self.match(RustParser.T__13)
                self.state = 150
                self.match(RustParser.Number)
                self.state = 151
                self.match(RustParser.RBRACK)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 153
                self.match(RustParser.LBRACK)
                self.state = 154
                self.type_()
                self.state = 155
                self.match(RustParser.RBRACK)
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = RustParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            self.match(RustParser.T__1)
            self.state = 163
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 160
                    self.statement() 
                self.state = 165
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 701488422715968) != 0):
                self.state = 166
                self.returnStmt()


            self.state = 169
            self.match(RustParser.T__2)
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = RustParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_statement)
        try:
            self.state = 176
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 171
                self.letStmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 172
                self.assignStmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 173
                self.forStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 174
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 175
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

        def varDef(self):
            return self.getTypedRuleContext(RustParser.VarDefContext,0)


        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_letStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetStmt" ):
                listener.enterLetStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetStmt" ):
                listener.exitLetStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetStmt" ):
                return visitor.visitLetStmt(self)
            else:
                return visitor.visitChildren(self)




    def letStmt(self):

        localctx = RustParser.LetStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_letStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(RustParser.T__14)
            self.state = 179
            self.varDef()
            self.state = 180
            self.match(RustParser.T__15)
            self.state = 181
            self.expression(0)
            self.state = 182
            self.match(RustParser.T__13)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def mutableDef(self):
            return self.getTypedRuleContext(RustParser.MutableDefContext,0)


        def immutableDef(self):
            return self.getTypedRuleContext(RustParser.ImmutableDefContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_varDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDef" ):
                listener.enterVarDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDef" ):
                listener.exitVarDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDef" ):
                return visitor.visitVarDef(self)
            else:
                return visitor.visitChildren(self)




    def varDef(self):

        localctx = RustParser.VarDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_varDef)
        try:
            self.state = 186
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 184
                self.mutableDef()
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 2)
                self.state = 185
                self.immutableDef()
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


    class ImmutableDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def type_(self):
            return self.getTypedRuleContext(RustParser.TypeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_immutableDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImmutableDef" ):
                listener.enterImmutableDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImmutableDef" ):
                listener.exitImmutableDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImmutableDef" ):
                return visitor.visitImmutableDef(self)
            else:
                return visitor.visitChildren(self)




    def immutableDef(self):

        localctx = RustParser.ImmutableDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_immutableDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.match(RustParser.Identifier)
            self.state = 191
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 189
                self.match(RustParser.T__3)
                self.state = 190
                self.type_()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MutableDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def type_(self):
            return self.getTypedRuleContext(RustParser.TypeContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_mutableDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMutableDef" ):
                listener.enterMutableDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMutableDef" ):
                listener.exitMutableDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMutableDef" ):
                return visitor.visitMutableDef(self)
            else:
                return visitor.visitChildren(self)




    def mutableDef(self):

        localctx = RustParser.MutableDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_mutableDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.match(RustParser.T__16)
            self.state = 194
            self.match(RustParser.Identifier)
            self.state = 197
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 195
                self.match(RustParser.T__3)
                self.state = 196
                self.type_()


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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStmt" ):
                return visitor.visitAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def assignStmt(self):

        localctx = RustParser.AssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_assignStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            self.expression(0)
            self.state = 200
            self.match(RustParser.T__15)
            self.state = 201
            self.expression(0)
            self.state = 202
            self.match(RustParser.T__13)
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStmt" ):
                return visitor.visitForStmt(self)
            else:
                return visitor.visitChildren(self)




    def forStmt(self):

        localctx = RustParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_forStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            self.match(RustParser.T__17)
            self.state = 205
            self.match(RustParser.Identifier)
            self.state = 206
            self.match(RustParser.T__18)
            self.state = 207
            self.expression(0)
            self.state = 208
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = RustParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            self.match(RustParser.T__19)
            self.state = 211
            self.expression(0)
            self.state = 212
            self.block()
            self.state = 215
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21:
                self.state = 213
                self.match(RustParser.T__20)
                self.state = 214
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStmt" ):
                return visitor.visitExprStmt(self)
            else:
                return visitor.visitChildren(self)




    def exprStmt(self):

        localctx = RustParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_exprStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
            self.expression(0)
            self.state = 218
            self.match(RustParser.T__13)
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = RustParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_returnStmt)
        try:
            self.state = 225
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 220
                self.match(RustParser.T__21)
                self.state = 221
                self.expression(0)
                self.state = 222
                self.match(RustParser.T__13)
                pass
            elif token in [6, 9, 41, 42, 43, 44, 45, 46, 49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 224
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

        def literal(self):
            return self.getTypedRuleContext(RustParser.LiteralContext,0)


        def primaryExpression(self):
            return self.getTypedRuleContext(RustParser.PrimaryExpressionContext,0)


        def macroCall(self):
            return self.getTypedRuleContext(RustParser.MacroCallContext,0)


        def borrowExpression(self):
            return self.getTypedRuleContext(RustParser.BorrowExpressionContext,0)


        def Identifier(self):
            return self.getToken(RustParser.Identifier, 0)

        def argumentList(self):
            return self.getTypedRuleContext(RustParser.ArgumentListContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RustParser.ExpressionContext,i)


        def LBRACK(self):
            return self.getToken(RustParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(RustParser.RBRACK, 0)

        def getRuleIndex(self):
            return RustParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RustParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 42
        self.enterRecursionRule(localctx, 42, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 239
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.state = 228
                self.literal()
                pass

            elif la_ == 2:
                self.state = 229
                self.primaryExpression()
                pass

            elif la_ == 3:
                self.state = 230
                self.macroCall()
                pass

            elif la_ == 4:
                self.state = 231
                self.borrowExpression()
                pass

            elif la_ == 5:
                self.state = 232
                self.match(RustParser.Identifier)
                self.state = 233
                self.match(RustParser.T__39)
                self.state = 234
                self.match(RustParser.T__5)
                self.state = 236
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 701488418521664) != 0):
                    self.state = 235
                    self.argumentList()


                self.state = 238
                self.match(RustParser.T__6)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 271
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,23,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 269
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
                    if la_ == 1:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 241
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 242
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1056965120) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 243
                        self.expression(6)
                        pass

                    elif la_ == 2:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 244
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 245
                        self.match(RustParser.T__29)
                        self.state = 246
                        self.expression(5)
                        pass

                    elif la_ == 3:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 247
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 248
                        self.match(RustParser.T__30)
                        self.state = 249
                        self.expression(4)
                        pass

                    elif la_ == 4:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 250
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 251
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1095216660480) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 252
                        self.expression(3)
                        pass

                    elif la_ == 5:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 253
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 254
                        self.match(RustParser.LBRACK)
                        self.state = 255
                        self.expression(0)
                        self.state = 256
                        self.match(RustParser.RBRACK)
                        pass

                    elif la_ == 6:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 258
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 259
                        self.match(RustParser.T__22)
                        self.state = 260
                        self.match(RustParser.Identifier)
                        pass

                    elif la_ == 7:
                        localctx = RustParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 261
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 262
                        self.match(RustParser.T__22)
                        self.state = 263
                        self.match(RustParser.Identifier)
                        self.state = 264
                        self.match(RustParser.T__5)
                        self.state = 266
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 701488418521664) != 0):
                            self.state = 265
                            self.argumentList()


                        self.state = 268
                        self.match(RustParser.T__6)
                        pass

             
                self.state = 273
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,23,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class BorrowExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(RustParser.ExpressionContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_borrowExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBorrowExpression" ):
                listener.enterBorrowExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBorrowExpression" ):
                listener.exitBorrowExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBorrowExpression" ):
                return visitor.visitBorrowExpression(self)
            else:
                return visitor.visitChildren(self)




    def borrowExpression(self):

        localctx = RustParser.BorrowExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_borrowExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 274
            self.match(RustParser.T__8)
            self.state = 275
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpression" ):
                return visitor.visitPrimaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def primaryExpression(self):

        localctx = RustParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_primaryExpression)
        self._la = 0 # Token type
        try:
            self.state = 289
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 277
                self.literal()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 278
                self.match(RustParser.Identifier)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 279
                self.match(RustParser.Identifier)
                self.state = 280
                self.match(RustParser.T__5)
                self.state = 282
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 701488418521664) != 0):
                    self.state = 281
                    self.argumentList()


                self.state = 284
                self.match(RustParser.T__6)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 285
                self.match(RustParser.T__5)
                self.state = 286
                self.expression(0)
                self.state = 287
                self.match(RustParser.T__6)
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


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RustParser.COMMA)
            else:
                return self.getToken(RustParser.COMMA, i)

        def getRuleIndex(self):
            return RustParser.RULE_argumentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgumentList" ):
                listener.enterArgumentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgumentList" ):
                listener.exitArgumentList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgumentList" ):
                return visitor.visitArgumentList(self)
            else:
                return visitor.visitChildren(self)




    def argumentList(self):

        localctx = RustParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 291
            self.expression(0)
            self.state = 296
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==51:
                self.state = 292
                self.match(RustParser.COMMA)
                self.state = 293
                self.expression(0)
                self.state = 298
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacroCall" ):
                return visitor.visitMacroCall(self)
            else:
                return visitor.visitChildren(self)




    def macroCall(self):

        localctx = RustParser.MacroCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_macroCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 299
            self.match(RustParser.Identifier)
            self.state = 300
            self.match(RustParser.T__39)
            self.state = 301
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

        def LBRACK(self):
            return self.getToken(RustParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(RustParser.RBRACK, 0)

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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacroArgs" ):
                return visitor.visitMacroArgs(self)
            else:
                return visitor.visitChildren(self)




    def macroArgs(self):

        localctx = RustParser.MacroArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_macroArgs)
        self._la = 0 # Token type
        try:
            self.state = 313
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [49]:
                self.enterOuterAlt(localctx, 1)
                self.state = 303
                self.match(RustParser.LBRACK)
                self.state = 305
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 701488418521664) != 0):
                    self.state = 304
                    self.macroInner()


                self.state = 307
                self.match(RustParser.RBRACK)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 308
                self.match(RustParser.T__5)
                self.state = 310
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 701488418521664) != 0):
                    self.state = 309
                    self.macroInner()


                self.state = 312
                self.match(RustParser.T__6)
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacroInner" ):
                return visitor.visitMacroInner(self)
            else:
                return visitor.visitChildren(self)




    def macroInner(self):

        localctx = RustParser.MacroInnerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_macroInner)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 315
            self.expression(0)
            self.state = 318
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 316
                self.match(RustParser.T__13)
                self.state = 317
                self.expression(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def POUND(self):
            return self.getToken(RustParser.POUND, 0)

        def LBRACK(self):
            return self.getToken(RustParser.LBRACK, 0)

        def attrInner(self):
            return self.getTypedRuleContext(RustParser.AttrInnerContext,0)


        def RBRACK(self):
            return self.getToken(RustParser.RBRACK, 0)

        def getRuleIndex(self):
            return RustParser.RULE_attribute

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttribute" ):
                listener.enterAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttribute" ):
                listener.exitAttribute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttribute" ):
                return visitor.visitAttribute(self)
            else:
                return visitor.visitChildren(self)




    def attribute(self):

        localctx = RustParser.AttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_attribute)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 320
            self.match(RustParser.POUND)
            self.state = 321
            self.match(RustParser.LBRACK)
            self.state = 322
            self.attrInner()
            self.state = 323
            self.match(RustParser.RBRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttrInnerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self, i:int=None):
            if i is None:
                return self.getTokens(RustParser.Identifier)
            else:
                return self.getToken(RustParser.Identifier, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RustParser.COMMA)
            else:
                return self.getToken(RustParser.COMMA, i)

        def getRuleIndex(self):
            return RustParser.RULE_attrInner

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttrInner" ):
                listener.enterAttrInner(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttrInner" ):
                listener.exitAttrInner(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttrInner" ):
                return visitor.visitAttrInner(self)
            else:
                return visitor.visitChildren(self)




    def attrInner(self):

        localctx = RustParser.AttrInnerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_attrInner)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 325
            self.match(RustParser.Identifier)
            self.state = 338
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 326
                self.match(RustParser.T__5)
                self.state = 335
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==45:
                    self.state = 327
                    self.match(RustParser.Identifier)
                    self.state = 332
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==51:
                        self.state = 328
                        self.match(RustParser.COMMA)
                        self.state = 329
                        self.match(RustParser.Identifier)
                        self.state = 334
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 337
                self.match(RustParser.T__6)


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

        def arrayLiteral(self):
            return self.getTypedRuleContext(RustParser.ArrayLiteralContext,0)


        def Number(self):
            return self.getToken(RustParser.Number, 0)

        def Binary(self):
            return self.getToken(RustParser.Binary, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(RustParser.StringLiteralContext,0)


        def booleanLiteral(self):
            return self.getTypedRuleContext(RustParser.BooleanLiteralContext,0)


        def getRuleIndex(self):
            return RustParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = RustParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_literal)
        try:
            self.state = 345
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [49]:
                self.enterOuterAlt(localctx, 1)
                self.state = 340
                self.arrayLiteral()
                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 2)
                self.state = 341
                self.match(RustParser.Number)
                pass
            elif token in [44]:
                self.enterOuterAlt(localctx, 3)
                self.state = 342
                self.match(RustParser.Binary)
                pass
            elif token in [41]:
                self.enterOuterAlt(localctx, 4)
                self.state = 343
                self.stringLiteral()
                pass
            elif token in [42, 43]:
                self.enterOuterAlt(localctx, 5)
                self.state = 344
                self.booleanLiteral()
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


    class BooleanLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(RustParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(RustParser.FALSE, 0)

        def getRuleIndex(self):
            return RustParser.RULE_booleanLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanLiteral" ):
                listener.enterBooleanLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanLiteral" ):
                listener.exitBooleanLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanLiteral" ):
                return visitor.visitBooleanLiteral(self)
            else:
                return visitor.visitChildren(self)




    def booleanLiteral(self):

        localctx = RustParser.BooleanLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_booleanLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 347
            _la = self._input.LA(1)
            if not(_la==42 or _la==43):
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


    class ArrayLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(RustParser.LBRACK, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RustParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RustParser.ExpressionContext,i)


        def RBRACK(self):
            return self.getToken(RustParser.RBRACK, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RustParser.COMMA)
            else:
                return self.getToken(RustParser.COMMA, i)

        def getRuleIndex(self):
            return RustParser.RULE_arrayLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayLiteral" ):
                listener.enterArrayLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayLiteral" ):
                listener.exitArrayLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayLiteral" ):
                return visitor.visitArrayLiteral(self)
            else:
                return visitor.visitChildren(self)




    def arrayLiteral(self):

        localctx = RustParser.ArrayLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_arrayLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 349
            self.match(RustParser.LBRACK)
            self.state = 350
            self.expression(0)
            self.state = 355
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==51:
                self.state = 351
                self.match(RustParser.COMMA)
                self.state = 352
                self.expression(0)
                self.state = 357
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 358
            self.match(RustParser.RBRACK)
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

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteral" ):
                return visitor.visitStringLiteral(self)
            else:
                return visitor.visitChildren(self)




    def stringLiteral(self):

        localctx = RustParser.StringLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_stringLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 360
            self.match(RustParser.T__40)
            self.state = 364
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,36,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 361
                    self.matchWildcard() 
                self.state = 366
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,36,self._ctx)

            self.state = 367
            self.match(RustParser.T__40)
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
        self._predicates[21] = self.expression_sempred
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
         




