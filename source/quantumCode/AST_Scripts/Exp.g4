grammar Exp;

program: exp (';' exp)* ;

exp: Identifier | letexp | callexp | ifexp | skipexp | xgexp | cuexp 
   | rzexp | srexp | lshiftexp | rshiftexp | revexp | qftexp | rqftexp | '(' program ')' ;
        
vexp: Identifier | numexp | boolexp | addexp | subexp | multexp | divexp | modexp | expexp;

bexp: lessexp | equalexp | greaterexp | andexp | orexp;        
        
posiexp : '(' vexp ','  vexp  ')' ;

skipexp: SKIPEXP posiexp;

xgexp: Xgate posiexp;
       
cuexp: CU posiexp exp;
       
rzexp: RZ vexp posiexp;

srexp: SR vexp vexp;

lshiftexp: Lshift vexp;

rshiftexp: Rshift vexp;

revexp: Rev vexp;

qftexp: QFT vexp vexp;
       
rqftexp: RQFT vexp vexp;
                                            
numexp: Number | '-' Number | Number Dot Number | '-' Number Dot Number;       
  
addexp:  exp '+' exp;
 
subexp: exp '-' exp;

multexp: exp '*'  exp;
 
divexp: exp '/' exp;
        
modexp: exp '%' exp;

expexp: exp '^' exp;


letexp: 'let' Identifier ( '(' Identifier ':' typea ')' )+ '=' exp;

matchexp: Match exp With ( '|' exp '=>' exp )+;

boolexp: TrueLiteral | FalseLiteral;

callexp: App exp exp;

ifexp: If bexp Then exp Else exp;

lessexp: exp Less exp;

equalexp: exp Equal exp;

greaterexp: exp Greater exp;


andexp: exp '&&'  exp;

orexp: exp '||' exp;


typea: booleantype | funct | numtype | pairtype;

booleantype: 'bool';

numtype: 'num';
        
pairtype: '(' typea ',' typea ')';


funct: '(' typea '->' typea ')';
        
 // Lexical Specification of this Programming Language
 //  - lexical specification rules start with uppercase

 App: 'app';
 Then: 'then';
 Else: 'else';
 Match : 'match' ;
 With : 'with' ;
 //Fun : 'Fun' ;
 If : 'if' ; 
 Car : 'car' ; 
 Cdr : 'cdr' ; 
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
 SR : 'SR';
 Lshift : 'Lshift';
 Rshift : 'Rshift';
 Rev : 'Rev';
 QFT : 'QFT';
 RQFT : 'RQFT';
 
 //Free : 'free' ;
 //Fork : 'fork' ;
 //Lock : 'lock' ;
 //UnLock : 'unlock' ;
 //Process : 'process' ;
 //Send : 'send' ;
 //Stop : 'stop' ;

 Dot : '.' ;

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
