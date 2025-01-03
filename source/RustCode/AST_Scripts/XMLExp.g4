grammar XMLExp;

program: (functionstmt)+;

stmt: letstmt | exp | printstmt | blockstmt | ifstmt | breakstmt | returnstmt | loopstmt | forstmt | matchstmt;

blockstmt: '<' STMT 'type' '=' '\'' Block '\'' '>' program '</' STMT '>' ;

letstmt : '<' STMT 'type' '=' '\'' Let '\'' (Mut ?)? ID '=' '\'' Identifier '\'' (':' atype)? '>' (exp | arrayexp) '</' STMT '>' ;

matchstmt: '<' STMT 'type' '=' '\'' Match '\'' '\'' Identifier '\'' '>' blockstmt '</' STMT '>';

printstmt: '<' STMT 'type' '=' '\'' Print '\'' '>' stringval (exp?) '</' STMT '>' ;

ifstmt: '<' STMT 'type' '=' '\'' IF '\'' '>' vexp blockstmt blockstmt '</' STMT '>' ;

ifletstmt: '<' STMT 'type' '=' '\'' Iflet '\'' ID '=' '\'' Identifier '\'' '>' vexp blockstmt blockstmt '</' STMT '>' ;

breakstmt: '<' STMT 'type' '=' '\'' Break '\'' '>' (vexp?) '</' STMT '>' ;

returnstmt: '<' STMT 'type' '=' '\'' Return '\'' '>' (vexp | idexp)? '</' STMT '>' ;

loopstmt: '<' STMT 'type' '=' '\'' Loop '\'' '>' blockstmt '</' STMT '>' ;

forstmt: '<' STMT 'type' '=' '\'' For '\'' ID '=' '\'' Identifier '\'' '>' '<range>' range_expr '</range>' blockstmt '</' STMT '>' ;

vectorstmt: '<' STMT 'type' '=' '\'' Vector '\'' '=' '\'' atype '\'' '>' (numexp+ | stringval+ | ()) '</' STMT '>' ;

functionstmt: '<' STMT 'type' '=' '\'' Function '\'' ID '=' '\'' Identifier '\'' '>' parameters blockstmt '</' STMT '>' ;

parameters: '<parameters>' (idexp (',' idexp)*)? '</parameters>' ;

exp: vexp | funccallexp | macroexp;

stringval : '<' VEXP OP '=' '\'' String '\'' '>' (StrLiteral | Identifier) '</' VEXP '>';

numexp: Number | Minus Number | HexLiteral | BinaryLiteral;

arrayexp: '[' (numexp (',' numexp)*)? ']';

atype: Int | Bool;

idexp : '<' VEXP OP '=' '\'' ID '\'' ('type' '=' '\'' atype '\'')? '>' Identifier '</' VEXP '>' ;

funccallexp: '<' VEXP OP '=' '\'' Call '\'' '>' Identifier '(' (vexp (',' vexp)*)? ')' '</' VEXP '>';

macroexp: '<' VEXP OP '=' '\'' Macro '\'' '>' Identifier '(' (vexp (',' vexp)*)? ')' '</' VEXP '>';

vexp: idexp
    | stringval
    | '<' VEXP OP '=' '\'' NUM '\'' '>' numexp '</' VEXP '>'
    | '<' VEXP OP '=' '\'' Bool '\'' '>' (TrueLiteral | FalseLiteral) '</' VEXP '>'
    | '<' VEXP OP '=' '\'' op '\'' '>' vexp vexp '</' VEXP '>'
    | '<' VEXP OP '=' '\'' sinop '\'' '>' vexp '</' VEXP '>'
    | '<' VEXP OP '=' '\'' Index '\'' '>' vexp '[' vexp ']' '</' VEXP '>';

range_expr: vexp '..' vexp;

// Lexical Specification of this Programming Language
op: Plus | Minus | Times | Div | Mod | Exp | And | Less | Equal | Or | Range | '>>' | '<<' | '&';

sinop : Reference;

TrueLiteral : '#t' ;
FalseLiteral : '#f' ;
Dot : '.' ;

HexLiteral : '0x' [0-9a-fA-F]+ ;
BinaryLiteral : '0b' [01]+ ;

RQFT : 'RQFT' ;

OP : 'op';

Plus : '+';

Minus : '-';

Times : '*';

Div : '/';

Mod : '%';

Exp : '^';

And : '&&';

Or : '||';

Less : '<';

Range : '..';

Equal : '==';

Reference : '&';

Type : 'type';

STMT : 'stmt';

PEXP : 'pexp';

VEXP : 'vexp';

IF : 'if';

Iflet: 'iflet';

Block : 'block';

Break : 'break';

Match : 'match';

Return : 'return';

Loop : 'loop';

For : 'for';

Vector : 'vec';

Function : 'fn';

ID : 'id';

Mut: 'mut';

Let : 'let';

Int : 'int';

Bool : 'bool';

Value : 'value';

String : 'string';

Print : 'print';

Number : DIGIT+ ;

NUM: 'num';

Identifier :   Letter LetterOrDigit*;

Letter :   [a-zA-Z$_];

LetterOrDigit: [a-zA-Z0-9$_];

fragment DIGIT: ('0'..'9');

fragment ESCQUOTE : '\\"';
StrLiteral :   '"' ( ESCQUOTE | ~('\n'|'\r') )*? '"';

AT : '@';
ELLIPSIS : '...';
WS  :  [ \t\r\n\u000C]+ -> skip;
Comment :   '/*' .*? '*/' -> skip;
Line_Comment :   '//' ~[\r\n]* -> skip;
