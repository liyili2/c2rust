grammar XMLExp;

program: stmt (stmt)*;

stmt: letstmt | exp | printstmt | blockstmt | ifstmt | breakstmt | returnstmt | loopstmt | forstmt;

blockstmt: '<' STMT 'type' '=' '\'' Block '\'' '>' program '</' STMT '>' ;

letstmt : '<' STMT 'type' '=' '\'' Let '\'' ID '=' '\'' Identifier '\'' '>' exp '</' STMT '>' ;

printstmt: '<' STMT 'type' '=' '\'' Print '\'' '>' stringval exp '</' STMT '>' ;

ifstmt: '<' STMT 'type' '=' '\'' IF '\'' '>' vexp blockstmt blockstmt '</' STMT '>' ;

breakstmt: '<' STMT 'type' '=' '\'' Break '\'' '>' (vexp ?) '</' STMT '>' ;

returnstmt: '<' STMT 'type' '=' '\'' Return '\'' '>' (vexp ?) '</' STMT '>' ;

loopstmt: '<' STMT 'type' '=' '\'' Loop '\'' '>' blockstmt '</' STMT '>' ;

forstmt: '<' STMT 'type' '=' '\'' For '\'' ID '=' '\'' Identifier '\'' '>' vexp blockstmt '</' STMT '>' ;

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

op: Plus | Minus | Times | Div | Mod | Exp | And | Less | Equal | Or | Range;

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
