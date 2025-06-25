grammar Rust;

program: (topLevelItem)* ;

topLevelItem
    : topLevelDef
    | staticVarDecl
    | attributes
    | externBlock
    | useDecl
    | typeAlias;

useDecl: 'use' typePath ('{' (typePath? Identifier ','? )* '}' ',' )* ';';

topLevelDef: functionDef | structDef | interfaceDef | constDef | unionDef | unsafeDef;
typeAlias: visibility? 'type' Identifier '=' typeExpr ';';
interfaceDef: 'impl' Identifier '{' functionDef+ '}' ;

externBlock: 'extern' STRING_LITERAL '{' externItem* '}';
externItem
    : visibility? 'type' Identifier ';'
    | visibility? 'static' 'mut'? Identifier ':' typeExpr ';'
    | visibility? 'fn' Identifier '(' externParams? ')' 
        ('->' typeExpr)? ';';
externParams: externParam (',' externParam)* (',' '...')? | '...';
externParam: (UNDERSCORE | Identifier)? ':' (typeExpr | ELLIPSIS);

visibility: 'pub';
unsafeModifier: 'unsafe';
externAbi: 'extern' STRING_LITERAL?;

attributes: innerAttribute+ ;
innerAttribute: POUND (EXCL?) LBRACK attribute RBRACK;
attribute
    : Identifier
    | Identifier '=' attrValue
    | Identifier '(' attrArgs ')';
attrArgs: attrArg (',' attrArg)*;
attrArg: Identifier ('=' attrValue)?;
attrValue: STRING_LITERAL | Number | Identifier;

structDef: visibility? 'struct' Identifier '{' structField* '}';
structField: visibility? Identifier ':' typeExpr ','?;
structLiteral: Identifier '{' structLiteralField* '}' ;
structLiteralField: Identifier (':' expression)? ','? ;

functionDef: visibility? unsafeModifier? externAbi? 'fn' Identifier ('()' | '(' paramList? ')') '->'? typeExpr? block;
paramList: param (',' param)* (',')?;
param: '&'? 'mut'? Identifier (':' typeExpr)?;

constDef: visibility? 'const' Identifier ':' typeExpr '=' expression ';';
unionDef: visibility? 'union' Identifier  ((':' typeExpr '=' expression ';') | '{' unionField* '}');
unionField: visibility? Identifier ':' typeExpr ','?;
unsafeDef: visibility? 'unsafe' Identifier ':' typeExpr '=' expression ';';

typeExpr: basicType | pointerType;
pointerType: '*' ('mut' | 'const') (typeExpr)?;
basicType
    : 'i32'
    | 'String'
    | 'bool'
    | 'u8'
    | arrayType
    | typePath basicType
    | ( DOUBLE_COLON? '<' typeExpr (',' typeExpr)* '>' '()'? )
    | Identifier ('<' typeExpr (',' typeExpr)* '>')?
    | Identifier '<' typeExpr '>'
    | '&' typeExpr
    | '[' typeExpr ']'
    | Identifier;

typePath: Identifier DOUBLE_COLON | DOUBLE_COLON? Identifier (DOUBLE_COLON Identifier)* ;
arrayType: '[' basicType ';' Number ']' ;

block: '{' statement* returnStmt? '}';
unsafeBlock: unsafeModifier block;
statement
    : unsafeBlock
    | letStmt
    | conditionalAssignmentStmt
    | structLiteral
    | structDef
    | staticVarDecl
    | typeWrapper
    | assignStmt
    | compoundAssignment
    | forStmt
    | ifStmt 
    | callStmt
    | exprStmt
    | whileStmt
    | returnStmt
    | loopStmt
    | 'break' ';'
    | 'continue' ';'
    | matchStmt
    ;

conditionalAssignmentStmt: 'let'? (typeWrapper | expression) '=' expression 'else' block ';';
callStmt: expression callExpressionPostFix ';' ;
letStmt: 'let' varDef '=' expression ';' | 'let' varDef initBlock | 'let' '(' (varDef ','?)* ')' '=' '(' (expression ','?)* ')' ';';
varDef: 'ref'? 'mut'? Identifier (':' typeExpr)?;
compoundOp: '+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' ;
compoundAssignment: expression compoundOp expression ';' ;
matchStmt: 'match' expression '{' matchArm+ '}' ;
matchArm: matchPattern ('|' matchPattern)* '=>' (block | 'return' (expression)?);
matchPattern: byteLiteral | Number | UNDERSCORE | Identifier;
whileStmt: 'while' expression block;
initializer: initBlock | block | expression ;
staticVarDecl: visibility? 'static' 'mut'? Identifier ':' (typeExpr | Identifier) '=' initializer ';';
initBlock: '{' (Identifier ':' expression ',')* '}' ';' expression;
assignStmt: expression '=' expression ';';
forStmt: 'for' Identifier 'in' expression block;
ifStmt: 'if' expression block ('else if' expression block)* ('else' block)?;
exprStmt: expression ';';
returnStmt: 'return' (expression)? ';' | Identifier;
loopStmt: 'loop' block;

boxWrappwer: 'Box' typeExpr? '(' expression ')';
typeWrapper: 'Some' '(' expression ')' ;
boxWrapperPrefix: 'Box' typeExpr? ;
typeWrapperPrefix: 'Some' ;

expression
    : mutableExpression expression
    | primaryExpression
    | structLiteral
    | expression castExpressionPostFix
    | typePathExpression expression
    | parenExpression
    | structFieldDec
    | structDefInit
    | unaryOpes expression
    | borrowExpression
    | unsafeExpression
    | expression fieldAccessPostFix
    | expression typeAccessPostfix
    | basicTypeCastExpr
    | expression rangeSymbol expression
    | expression booleanOps expression
    | expression binaryOps expression
    | expression conditionalOps expression
    | expression compoundOps expression
    | expressionBlock
    | qualifiedExpression
    | expression callExpressionPostFix
    | patternPrefix expression
    | arrayDeclaration
    | dereferenceExpression
    ;

basicTypeCastExpr: typeExpr typePath;
unsafeExpression: 'unsafe' '{' expression '}' ;
qualifiedExpression: '<' expression '>';
typeAccessPostfix: typeExpr;
structDefInit: Identifier '=' '{' expression '}' ';' ;
arrayDeclaration: Identifier '!'? '[' Number ';' expression ']' ;
typePathExpression: (Identifier DOUBLE_COLON)+ ;
patternPrefix: 'let'? pattern '=' ;
pattern: 'ref'? 'mut'? Identifier | Identifier '(' 'ref'? 'mut'? Identifier ')' ;
castExpressionPostFix: 'as' typeExpr ('as' typeExpr)*;
compoundOps: '+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=';
rangeSymbol: '..';
conditionalOps: '==' | '!=' | '>' | '<' | '||' | '&&';
booleanOps: '>>' | '&' | '>=' | '<=';
binaryOps: '*' | '/' | '%' | '+' | '-' ;
structFieldDec: Identifier '{' structLiteralField (',' structLiteralField)* ','? '}' ;
mutableExpression: 'mut';
unaryOpes: '!' | '+' | '-';
parenExpression: '(' expression ')';
dereferenceExpression: '*' expression;
expressionBlock: '{' statement* expression '}';
borrowExpression: '&' expression;
primaryExpression: literal | Identifier;

fieldAccessPostFix: '[' primaryExpression ']' | ('.' primaryExpression)+;
callExpressionPostFix: '!'? functionCallArgs;
functionCallArgs: '()' | '(' expression (',' expression)* ')' ;

TRUE: 'true';
FALSE: 'false';
NONE: 'None';
literal: arrayLiteral | HexNumber | Number | SignedNumber | BYTE_STRING_LITERAL | 
         Binary | STRING_LITERAL | booleanLiteral | CHAR_LITERAL | byteLiteral |  NONE;
byteLiteral: 'b\'.\'' | 'b\'|\'' | 'b\'*\'' | 'b\'' LPAREN '\'' | 'b\'' RPAREN '\'' | 'b\'+\'' | 'b\'?\'';

booleanLiteral: TRUE | FALSE;
Binary: '0b' [0-1]+;
arrayLiteral: Identifier? '!'? '[' expression (',' expression)* ']' | Identifier? '!'? '[' expression ';' expression ']' | Identifier? '!'? '[' ']';
STRING_LITERAL: '"' (~["\\] | '\\' .)* '"';
stringLiteral: '"' .*? '"';
Identifier: [a-zA-Z_][a-zA-Z0-9_]*;
Number: [0-9]+;
SignedNumber: ('-' | '+') Number;
BYTE_STRING_LITERAL: 'b"' (~["\\\r\n] | '\\' .)* '"';
HexNumber: '0x' [0-9a-fA-F]+;
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
ELLIPSIS: '...';
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;