grammar XMLExp;

program: stmt+;

stmt: letstmt | exp | printstmt | blockstmt | ifstmt | breakstmt | returnstmt | loopstmt | forstmt | matchstmt | functionstmt;

blockstmt: '<blockstmt' 'type' '=' '\'' Block '\'' '>' program '</blockstmt>' ;

letstmt : '<letstmt' 'type' '=' '\'' Let '\'' (Mut ID)? '=' '\'' Identifier '\'' (':' atype)? '>' (exp | arrayexp) '</letstmt>' ;

matchstmt: '<matchstmt' 'type' '=' '\'' Match '\'' '\'' Identifier '\'' '>' blockstmt '</matchstmt>';

printstmt: '<printstmt' 'type' '=' '\'' Print '\'' '>' stringval (exp?) '</printstmt>' ;

ifstmt: '<ifstmt' 'type' '=' '\'' IF '\'' '>' vexp blockstmt blockstmt '</ifstmt>' ;

ifletstmt: '<ifletstmt' 'type' '=' '\'' Iflet '\'' ID '=' '\'' Identifier '\'' '>' vexp blockstmt blockstmt '</ifletstmt>' ;

breakstmt: '<breakstmt' 'type' '=' '\'' Break '\'' '>' (vexp?) '</breakstmt>' ;

returnstmt: '<returnstmt' 'type' '=' '\'' Return '\'' '>' (vexp | idexp)? '</returnstmt>' ;

loopstmt: '<loopstmt' 'type' '=' '\'' Loop '\'' '>' blockstmt '</loopstmt>' ;

forstmt: '<forstmt' 'type' '=' '\'' For '\'' ID '=' '\'' Identifier '\'' '>' '<range>' range_expr '</range>' blockstmt '</forstmt>' ;

vectorstmt: '<vectorstmt' 'type' '=' '\'' Vector '\'' '=' '\'' atype '\'' '>' (numexp+ | stringval+ | ()) '</vectorstmt>' ;

functionstmt: '<functionstmt' 'type' '=' '\'' Function '\'' ID '=' '\'' Identifier '\'' '>' parameters blockstmt '</functionstmt>' ;

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

Reference : '&amp;';

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

Identifier : Letter LetterOrDigit*;

Letter : [a-zA-Z$_];

LetterOrDigit: [a-zA-Z0-9$_];

fragment DIGIT: ('0'..'9');

fragment ESCQUOTE : '\\"';
StrLiteral :   '"' ( ESCQUOTE | ~('\n'|'\r') )*? '"';

AT : '@';
ELLIPSIS : '...';
WS  :  [ \t\r\n\u000C]+ -> skip;
Comment :   '/*' .*? '*/' -> skip;
Line_Comment :   '//' ~[\r\n]* -> skip;
