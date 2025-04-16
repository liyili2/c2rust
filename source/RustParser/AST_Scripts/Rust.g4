grammar Rust;

program: (functionDef)+;

functionDef: 'fn' Identifier '(' paramList? ')' '->'? type? block;

paramList: param (',' param)*;
param: Identifier ':' referenceType;

referenceType: '&' type;
type
    : 'i32'
    | 'Vec' '<' type '>'
    | '&' type
    | '[' type ';' Number ']'
    | '[' type ']' 
    ;

block: '{' statement* returnStmt? '}';

statement
    : letStmt
    | assignStmt
    | forStmt
    | ifStmt
    | exprStmt
    ;

letStmt: 'let' 'mut'? Identifier (':' type)? '=' expression ';';
assignStmt: expression '=' expression ';';
forStmt: 'for' Identifier 'in' expression block;
ifStmt: 'if' expression block ('else' block)?;
exprStmt: expression ';';
returnStmt: 'return' expression ';' | expression;

expression
    : primaryExpression
    | macroCall
    | '&' expression
    | expression '[' expression ']'                           
    | expression '.' Identifier                               
    | expression '.' Identifier '(' argumentList? ')'         
    | expression ('*' | '/' | '%' | '+' | '-' | '>>' | '&') expression   
    | expression '==' expression  
    | expression '..' expression
    | expression ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=') expression     
    | Identifier '!' '(' argumentList? ')'                       
    ;

primaryExpression
    : literal
    | Identifier
    | Identifier '(' argumentList? ')'                        
    | '(' expression ')'                                      
    ;

argumentList: expression (',' expression)*;

macroCall: Identifier '!' macroArgs;
macroArgs: '[' macroInner? ']' | '(' macroInner? ')';
macroInner: expression (';' expression)?;  // supports [value; count] form

literal: Number | Binary | arrayLiteral | stringLiteral;
Binary: '0b' [0-1]+;
arrayLiteral: '[' expression (',' expression)* ']';
stringLiteral: '"' .*? '"';

Identifier: [a-zA-Z_][a-zA-Z0-9_]*;
Number: [0-9]+;

WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;
