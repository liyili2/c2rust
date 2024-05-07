grammar XMLExp;

program: letstmt | exp | printstmt | blockstmt;

blockstmt: '<' STMT 'type' '=' '\'' Block '\'' '>' (program +) '</' STMT '>' ;

letstmt : '<' STMT 'type' '=' '\'' Let '\'' '>' idexp exp '</' STMT '>' ;

printstmt: '<' STMT 'type' '=' '\'' Print '\'' '>' stringval exp '</' STMT '>' ;

ifstmt: '<' STMT 'type' '=' '\'' IF '\'' '>' vexp blockstmt blockstmt '</' STMT '>' ;

breakstmt: '<' STMT 'type' '=' '\'' Break '\'' '>' (vexp ?) '</' STMT '>' ;

returnstmt: '<' STMT 'type' '=' '\'' Return '\'' '>' (vexp ?) '</' STMT '>' ;

loopstmt: '<' STMT 'type' '=' '\'' Loop '\'' '>' blockstmt '</' STMT '>' ;

forstmt: '<' STMT 'type' '=' '\'' For '\'' '>' idexp vexp blockstmt '</' STMT '>' ;

exp: vexp ;

idexp : '<' ID '>' Identifier '</' ID '>';

stringval : '<' Value '>' StrLiteral '</' Value '>';

vexp: idexp | '<' VEXP '>' numexp '</' VEXP '>'
    | '<' VEXP '>' boolexp '</' VEXP '>' | '<' VEXP OP '=' '\'' op '\'' '>' vexp vexp '</' VEXP '>';

numexp: Number | Minus Number;
        
 // Lexical Specification of this Programming Language
 //  - lexical specification rules start with uppercase

op: Plus | Minus | Times | Div | Mod | Exp | And | Less | Equal | Or | Range;

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

 And : '&&';

 Or : '||';

 Less : '<';

 Range : '..';

 Equal : '==';

 Type : 'type';

 STMT : 'stmt';

 PEXP : 'pexp';

 VEXP : 'vexp';

 IF : 'if';

 Block : 'block';

 Break : 'break';

 Return : 'return';

 Loop : 'loop';

 For : 'for';

 ID : 'id';

 Let : 'let';

 Value : 'value';

 Print : 'print';

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
