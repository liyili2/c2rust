grammar XMLExp;

program: exp (exp)* ;

exp: skipexp | xexp | cuexp | rzexp | srexp | lshiftexp | rshiftexp | revexp | qftexp | rqftexp;

idexp : '<' ID '>' Identifier '</' ID '>';
        
vexp: idexp | '<' VEXP '>' numexp '</' VEXP '>'
    | '<' VEXP '>' boolexp '</' VEXP '>' | '<' VEXP OP '=' '\'' op '\'' '>' vexp vexp '</' VEXP '>';

numexp: Number | Minus Number;
        
 // Lexical Specification of this Programming Language
 //  - lexical specification rules start with uppercase

skipexp: '<' PEXP 'gate' '=' '\'' 'SKIP' '\'' '>' idexp vexp '</' PEXP '>' ;

xexp: '<' PEXP 'gate' '=' '\'' 'X' '\'' '>' idexp vexp '</' PEXP '>' ;

cuexp: '<' PEXP 'gate' '=' '\'' 'CU' '\'' '>' idexp vexp program '</' PEXP '>' ;

rzexp: '<' PEXP 'gate' '=' '\'' 'RZ' '\'' '>' vexp idexp vexp '</' PEXP '>' ;

srexp: '<' PEXP 'gate' '=' '\'' 'SR' '\'' '>' vexp idexp '</' PEXP '>' ;

lshiftexp: '<' PEXP 'gate' '=' '\'' 'Lshift' '\'' '>' idexp '</' PEXP '>' ;

rshiftexp: '<' PEXP 'gate' '=' '\'' 'Rshift' '\'' '>' idexp '</' PEXP '>' ;

revexp: '<' PEXP 'gate' '=' '\'' 'Rev' '\'' '>' idexp '</' PEXP '>' ;

qftexp: '<' PEXP 'gate' '=' '\'' 'QFT' '\'' '>' idexp vexp '</' PEXP '>' ;

rqftexp: '<' PEXP 'gate' '=' '\'' 'RQFT' '\'' '>' idexp vexp '</' PEXP '>' ;

op: Plus | Minus | Times | Div | Mod | Exp;

boolexp: TrueLiteral | FalseLiteral;

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

 Type : 'type';

 PEXP : 'pexp';

 VEXP : 'vexp';

 ID : 'id';

 Number : DIGIT+ ;



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
