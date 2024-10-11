grammar XMLExp;

program: stmt (stmt)*;

stmt: letstmt | exp | printstmt | blockstmt | ifstmt | breakstmt | returnstmt | loopstmt | forstmt | matchstmt;

blockstmt: '<' STMT 'type' '=' '\'' Block '\'' '>' program '</' STMT '>' ;

letstmt : '<' STMT 'type' '=' '\'' Let '\'' (Mut ?) ID '=' '\'' Identifier '\'' '>' exp '</' STMT '>' ;

matchstmt: '<' STMT 'type' '=' '\'' Match '\'' '\'' Identifier '\'' '>' blockstmt '</' STMT '>';

printstmt: '<' STMT 'type' '=' '\'' Print '\'' '>' stringval exp '</' STMT '>' ;

ifstmt: '<' STMT 'type' '=' '\'' IF '\'' '>' vexp blockstmt blockstmt '</' STMT '>' ;

ifletstmt: '<' STMT 'type' '=' '\'' Iflet '\'' ID '=' '\'' Identifier '\'' '>' vexp blockstmt blockstmt '</' STMT '>' ;

breakstmt: '<' STMT 'type' '=' '\'' Break '\'' '>' (vexp ?) '</' STMT '>' ;

returnstmt: '<' STMT 'type' '=' '\'' Return '\'' '>' (vexp ?) '</' STMT '>' ;

loopstmt: '<' STMT 'type' '=' '\'' Loop '\'' '>' blockstmt '</' STMT '>' ;

forstmt: '<' STMT 'type' '=' '\'' For '\'' ID '=' '\'' Identifier '\'' '>' vexp blockstmt '</' STMT '>' ;

vectorstmt: '<' STMT 'type' '=' '\'' Vector '\'' '=' '\'' atype '\'' '>' (numexp+) | (stringval+) | () '</' STMT '>' ;

functionstmt: '<' STMT 'type' '=' '\'' Function '\'' ID '=' '\'' Identifier '\'' '>' (idexp+) blockstmt '</' STMT '>' ;

exp: vexp ;

stringval : '<' VEXP OP '=' '\'' String '\'' '>' StrLiteral '</' VEXP '>';

numexp: Number | Minus Number;

atype: Int | Bool;

idexp : '<' VEXP OP '=' '\'' ID '\'' ('type' '=' '\'' atype '\'')? '>' Identifier '</' VEXP '>' ;

vexp: idexp
    | stringval
    | '<' VEXP OP '=' '\'' NUM '\'' '>' numexp '</' VEXP '>'
    | '<' VEXP OP '=' '\'' Bool '\'' '>' (TrueLiteral | FalseLiteral) '</' VEXP '>'
    | '<' VEXP OP '=' '\'' op '\'' '>' vexp vexp '</' VEXP '>';


 // Lexical Specification of this Programming Language
 //  - lexical specification rules start with uppercase

op: Plus | Minus | Times | Div | Mod | Exp | And | Less | Equal | Or | Range | Reference ;

 TrueLiteral : '#t' ;
 FalseLiteral : '#f' ;
 Dot : '.' ;

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
