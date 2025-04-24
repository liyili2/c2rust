grammar Rust;

program: (topLevelItem)* ;

topLevelItem
    : functionDef
    | structDef
    | attribute
    ;

structDef
    : 'struct' Identifier '{' structField* '}'
    ;

structField
    : Identifier ':' type ','?
    ;

functionDef: 'fn' Identifier '(' paramList? ')' '->'? type? block;

paramList: param (',' param)*;
param: Identifier ':' referenceType;

referenceType: '&' type;
type
    : basicType
    ;

basicType
    : 'i32'
    | 'String'
    | 'bool'
    | Identifier ('<' type (',' type)* '>')?
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
    : literal
    | primaryExpression
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

attribute
    : POUND LBRACK attrInner RBRACK
    ;

attrInner
    : Identifier ( '(' (Identifier (COMMA Identifier)*)? ')' )?
    ;

TRUE: 'true';
FALSE: 'false';

literal: arrayLiteral | Number | Binary | stringLiteral | booleanLiteral;
booleanLiteral: TRUE | FALSE;
Binary: '0b' [0-1]+;
arrayLiteral: '[' expression (',' expression)* ']';
stringLiteral: '"' .*? '"';
Identifier: [a-zA-Z_][a-zA-Z0-9_]*;
Number: [0-9]+;

GT: '>'; // make sure this comes FIRST
POUND: '#';
LBRACK: '[';
RBRACK: ']';
COMMA: ',';

WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;
