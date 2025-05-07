grammar Rust;

program: (topLevelItem)* ;

topLevelItem
    : functionDef
    | structDef
    | attributes
    | externBlock
    | typeAlias
    | constDef
    | unionDef
    | unsafeDef
    | staticVarDecl
    ;

typeAlias: visibility? 'type' Identifier '=' type ';';
externBlock: 'extern' STRING_LITERAL '{' externItem* '}';

externItem
    : visibility? 'type' Identifier ';'
    | visibility? 'static' 'mut'? Identifier ':' type ';'
    | visibility? 'fn' Identifier '(' externParams? ')' 
        ('->' type)? ';'
    ;

externParams: externParam (',' externParam)* (',' '...')? | '...';
externParam: (UNDERSCORE | Identifier)? ':' (type | ELLIPSIS);

visibility: 'pub';
attributes: innerAttribute+ ;
innerAttribute: POUND  (EXCL?) LBRACK attribute RBRACK;
attribute: Identifier (LPAREN attrArgs RPAREN)?;
attrArgs: attrArg (COMMA attrArg)*;
attrArg: Identifier;
structDef: visibility? 'struct' Identifier '{' structField* '}';
structField: visibility? Identifier ':' type ','?;
functionDef: visibility? unsafeModifier? externAbi? 'fn' Identifier '(' paramList? ')' '->'? type? block;
unsafeModifier: 'unsafe';
externAbi: 'extern' STRING_LITERAL?;

paramList: param (',' param)* (',')?;
param: 'mut'? Identifier ':' type;

constDef: visibility? 'const' Identifier ':' type '=' expression ';';
unionDef: visibility? 'union' Identifier  ((':' type '=' expression ';') | '{' unionField* '}');
unionField: visibility? Identifier ':' type ','?;
unsafeDef: visibility? 'unsafe' Identifier ':' type '=' expression ';';
referenceType: '&' type;
type: basicType | pointerType;
typePath: DOUBLE_COLON? Identifier (DOUBLE_COLON Identifier)*;
pointerType: '*' ('mut' | 'const') type;
basicType
    : 'i32'
    | 'String'
    | 'bool'
    | '()'
    | typePath ('<' type (',' type)* '>')?
    | Identifier ('<' type (',' type)* '>')?
    | '&' type
    | typePath? '[' type ';' Number ']'
    | typePath
    | '[' type ']'
    | Identifier
    ;

block: '{' statement* returnStmt? '}';

statement
    : letStmt
    | staticVarDecl
    | assignStmt
    | Identifier ';'
    | expression ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=') expression ';'
    | forStmt
    | ifStmt
    | exprStmt
    | whileStmt
    | loopStmt
    | 'break' ';'
    | 'continue' ';'
    | 'match' expression '{' matchArm+ '}'
    ;

whileStmt: 'while' expression block;
staticVarDecl: visibility? 'static' 'mut'? Identifier ':' (type | Identifier) '=' initializer ';';
initializer: expression | block;
letStmt: 'let' varDef '=' expression ';';

varDef: 'ref' 'mut'? Identifier (':' type)?
    | 'mut' Identifier (':' type)?
    | Identifier (':' type)?;

assignStmt: expression '=' expression ';';
forStmt: 'for' Identifier 'in' expression block;
ifStmt: 'if' expression block ('else' block)?;
exprStmt: expression ';';
returnStmt: 'return' (expression)? ';' | expression;
loopStmt: 'loop' block;

expression
    : postfixExpression
    | literal
    | primaryExpression
    | '*' expression
    | macroCall
    | borrowExpression
    | typePath DOUBLE_COLON '<' type '>()'
    | expression '[' expression ']'
    | '!' expression
    | expression ('*' | '/' | '%' | '+' | '-' | '>>' | '&' | '>=' | '<=') expression
    | expression ('==' | '!=' | '>' | '<' | '||' | '&&') expression
    | expression '..' expression
    | expression ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=') expression
    | Identifier '!' '(' argumentList? ')'
    | expression 'as' type ('as' type)*
    | expressionBlock
    | '&' 'mut' expression
    | '(' expression ')'
    ;

expressionBlock: '{' statement* expression '}';
borrowExpression: '&' expression;
postfixExpression
  : primaryExpression
    (
      ('()' | '('argumentList?')')
    |  ('.' Identifier)+
    | '.' Identifier ( '(' argumentList? ')' | '()' )     // method call
    | '[' expression ']'                         // indexing
    )*
  ;

primaryExpression
    : literal
    | Identifier
    | qualifiedFunctionCall
    | Identifier '(' argumentList? ')'
    | '(' expression ')'
    | Identifier '{' structLiteralField (',' structLiteralField)* ','? '}'
    ;

qualifiedFunctionCall
  : DOUBLE_COLON typePath DOUBLE_COLON Identifier genericArgs? '(' argumentList? ')'
  ;

genericArgs
  : '<' type (',' type)* '>'
  ;
structLiteralField: Identifier ':' expression;
matchArm: matchPattern ('|' matchPattern)* '=>' block;
matchPattern: Number | UNDERSCORE | Identifier;
argumentList: expression (',' expression)*;
macroCall: Identifier '!' macroArgs;
macroArgs: '[' macroInner? ']' | '(' macroInner? ')';
macroInner: expression (';' expression)?;  // supports [value; count] form

TRUE: 'true';
FALSE: 'false';

literal: arrayLiteral | Number | SignedNumber | Binary | stringLiteral | booleanLiteral | CHAR_LITERAL;
booleanLiteral: TRUE | FALSE;
Binary: '0b' [0-1]+;
arrayLiteral: '[' expression (',' expression)* ']' | '[' expression ';' expression ']';
stringLiteral: '"' .*? '"';
Identifier: [a-zA-Z_][a-zA-Z0-9_]*;
Number: [0-9]+;
SignedNumber: ('-' | '+') Number;

CHAR_LITERAL: '\'' (~['\\\r\n] | '\\' .) '\'';
DOUBLE_COLON: '::';
EXCL: '!';
GT: '>'; // make sure this comes FIRST
POUND: '#';
LBRACK: '[';
RBRACK: ']';
COMMA: ',';
LPAREN: '(';
RPAREN: ')';
UNDERSCORE: '_';
COLON: ':';
STRING_LITERAL: '"' (~["\\] | '\\' .)* '"';
ELLIPSIS: '...';
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;
