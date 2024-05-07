grammar Exp;






 // Lexical Specification of this Programming Language
 //  - lexical specification rules start with uppercase

 Define : 'define' ;
 Let : 'let' ;
 Letrec : 'letrec' ;
 Lambda : 'lambda' ;
 If : 'if' ; 
 Car : 'car' ; 
 Cdr : 'cdr' ; 
 Cons : 'cons' ; 
 List : 'list' ; 
 Null : 'null?' ; 
 Less : '<' ;
 Equal : '=' ;
 Greater : '>' ;
 TrueLiteral : '#t' ;
 FalseLiteral : '#f' ;
// Ref : 'ref' ;
// Deref : 'deref' ;
// Assign : 'set!' ;

 SKIPEXP : 'SKIP';
 Xgate : 'X' ;
 CU : 'CU';
 RZ : 'RZ';
 RRZ : 'RRZ';
 SR : 'SR';
 SRR : 'SRR';
 Lshift : 'Lshift';
 Rshift : 'Rshift';
 Rev : 'Rev';
 QFT : 'QFT';
 RQFT : 'RQFT';
 Seq : ';';
 
 //Free : 'free' ;
 //Fork : 'fork' ;
 //Lock : 'lock' ;
 //UnLock : 'unlock' ;
 //Process : 'process' ;
 //Send : 'send' ;
 //Stop : 'stop' ;

 Self : 'self' ;
 Dot : '.' ;

 Number : DIGIT+ ;



 Identifier :   Letter LetterOrDigit*;

 Letter :   [a-zA-Z$_]
    |   ~[\u0000-\u00FF\uD800-\uDBFF] 
        {Character.isJavaIdentifierStart(_input.LA(-1))}?
    |   [\uD800-\uDBFF] [\uDC00-\uDFFF] 
        {Character.isJavaIdentifierStart(Character.toCodePoint((char)_input.LA(-2), (char)_input.LA(-1)))}? ;

 LetterOrDigit: [a-zA-Z0-9$_]
    |   ~[\u0000-\u00FF\uD800-\uDBFF] 
        {Character.isJavaIdentifierPart(_input.LA(-1))}?
    |    [\uD800-\uDBFF] [\uDC00-\uDFFF] 
        {Character.isJavaIdentifierPart(Character.toCodePoint((char)_input.LA(-2), (char)_input.LA(-1)))}?;

 fragment DIGIT: ('0'..'9');

 fragment ESCQUOTE : '\\"';
 StrLiteral :   '"' ( ESCQUOTE | ~('\n'|'\r') )*? '"';

 AT : '@';
 ELLIPSIS : '...';
 WS  :  [ \t\r\n\u000C]+ -> skip;
 Comment :   '/*' .*? '*/' -> skip;
 Line_Comment :   '//' ~[\r\n]* -> skip;
