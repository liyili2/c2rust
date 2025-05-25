grammar Rust;

program: (topLevelItem)* ;

topLevelItem
    : topLevelDef
    | staticVarDecl
    | attributes
    | externBlock
    | typeAlias;

topLevelDef: functionDef | structDef | interfaceDef |constDef | unionDef | unsafeDef;
typeAlias: visibility? 'type' Identifier '=' type ';';
interfaceDef: 'impl' Identifier '{' functionDef+ '}' ;

externBlock: 'extern' STRING_LITERAL '{' externItem* '}';
externItem
    : visibility? 'type' Identifier ';'
    | visibility? 'static' 'mut'? Identifier ':' type ';'
    | visibility? 'fn' Identifier '(' externParams? ')' 
        ('->' type)? ';';
externParams: externParam (',' externParam)* (',' '...')? | '...';
externParam: (UNDERSCORE | Identifier)? ':' (type | ELLIPSIS);

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
structField: visibility? Identifier ':' type ','?;
structLiteral: Identifier '{' structLiteralField* '}' ;

functionDef: visibility? unsafeModifier? externAbi? 'fn' Identifier ('()' | '(' paramList? ')') '->'? type? block;
paramList: param (',' param)* (',')?;
param: '&'? 'mut'? Identifier (':' type)?;

constDef: visibility? 'const' Identifier ':' type '=' expression ';';
unionDef: visibility? 'union' Identifier  ((':' type '=' expression ';') | '{' unionField* '}');
unionField: visibility? Identifier ':' type ','?;
unsafeDef: visibility? 'unsafe' Identifier ':' type '=' expression ';';

type: basicType | pointerType;
pointerType: '*' ('mut' | 'const') (type)?;
basicType
    : 'i32'
    | 'String'
    | 'bool'
    | 'u8'
    | '()'
    | typePath ('<' type (',' type)* '>')?
    | Identifier ('<' type (',' type)* '>')?
    | Identifier '<' type '>'
    | '&' type
    | typePath? '[' type ';' Number ']'
    | '[' type ']'
    | Identifier;
typePath: Identifier DOUBLE_COLON | DOUBLE_COLON? Identifier (DOUBLE_COLON Identifier)* ;

block: '{' statement* returnStmt? '}';
unsafeBlock: 'unsafe' block;
statement
    : letStmt
    | callStmt
    | structLiteral
    | staticVarDecl
    | assignStmt
    | compoundAssignment
    | forStmt
    | ifStmt
    | exprStmt
    | whileStmt
    | returnStmt
    | loopStmt
    | 'break' ';'
    | 'continue' ';'
    | matchStmt
    | qualifiedFunctionCall ('.' qualifiedFunctionCall)* ';'
    ;

callStmt: expression callExpressionPostFix ';' ;
letStmt: 'let' varDef '=' expression ';' | 'let' 'mut'? Identifier ':' (type | Identifier) '=' initializer ';' | 'let' varDef initBlock ;
varDef: 'ref' 'mut'? Identifier (':' type)? | 'mut' Identifier ((':' | '=') type)? | Identifier (':' type)?;
compoundOp: '+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' ;
compoundAssignment: expression compoundOp expression ';' ;
matchStmt: 'match' expression '{' matchArm+ '}' ;
whileStmt: 'while' expression block;
initializer: initBlock | block | expression ;
staticVarDecl: visibility? 'static' 'mut'? Identifier ':' (type | Identifier) '=' initializer ';';
initBlock: '{' (Identifier ':' expression ',')* '}' ';' expression;
assignStmt: expression '=' expression ';';
forStmt: 'for' Identifier 'in' expression block;
ifStmt: 'if' expression block ('else if' expression block)* ('else' block)?;
exprStmt: expression ';';
returnStmt: 'return' (expression)? ';' | Identifier;
loopStmt: 'loop' block;

expression
    : mutableExpression expression
    | primaryExpression
    | dereferenceExpression
    | typePathExpression
    | parenExpression
    | structFieldDec
    | unaryOpes expression
    | borrowExpression
    | expression fieldAccessPostFix
    | expression booleanOps expression
    | expression binaryOps expression
    | expression conditionalOps expression
    | expression patternSymbol expression
    | expression compoundOps expression
    | expression castExpressionPostFix
    | expressionBlock
    | expression callExpressionPostFix
    ;

typePathExpression: (Identifier DOUBLE_COLON)+ ;
patternPrefix: 'let'? pattern '=' ;
pattern: 'ref'? 'mut'? Identifier | 'Some' '(' 'ref'? 'mut'? Identifier ')' ;
castExpressionPostFix: 'as' type ('as' type)*;
compoundOps: '+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=';
patternSymbol: '..';
conditionalOps: '==' | '!=' | '>' | '<' | '||' | '&&';
booleanOps: '>>' | '&' | '>=' | '<=';
binaryOps: '*' | '/' | '%' | '+' | '-' ;
structFieldDec: Identifier '{' structLiteralField (',' structLiteralField)* ','? '}' ;
mutableExpression: 'mut';  
unaryOpes: '!' | '+' | '-';
parenExpression: '(' expression ')';
referenceExpression: '&' expression;
dereferenceExpression: '*' expression;
expressionBlock: '{' statement* expression '}';
borrowExpression: '&' expression;
primaryExpression: literal | Identifier;

fieldAccessPostFix: '[' primaryExpression ']' | ('.' primaryExpression)+;
callExpressionPostFix: expression functionCallArgs;
functionCallArgs: '(' expression (',' expression)* ')' ;
postfixExpression
  : primaryExpression
    (
      ('()' | '('argumentList?')')
    |  ('.' Identifier)+
    | '.' Identifier ( '(' argumentList? ')' | '()' )
    )+
  ;

qualifiedFunctionCall
  : DOUBLE_COLON typePath Identifier DOUBLE_COLON genericArgs? ('()' | '(' argumentList? ')') 
  | Identifier ('.' Identifier)* (DOUBLE_COLON Identifier)* ('()' | '(' ( Identifier '(' STRING_LITERAL ')' | argumentList)* ')')
  ;
macroCall: Identifier '!' macroArgs;
macroArgs: '[' macroInner? ']' | '(' macroInner? ')';
macroInner: expression (';' expression)?;  // supports [value; count] form

genericArgs: '<' type (',' type)* '>';
structLiteralField: Identifier (':' expression)? ',' ;
matchArm: matchPattern ('|' matchPattern)* '=>' block;
matchPattern: Number | UNDERSCORE | Identifier;
argumentList: (qualifiedFunctionCall | expression) (',' (qualifiedFunctionCall | expression))* (',')? | (DOUBLE_COLON Identifier)+ ('()' | '(' argumentList ')');

TRUE: 'true';
FALSE: 'false';
NONE: 'None';
literal: arrayLiteral | HexNumber | Number | SignedNumber | BYTE_STRING_LITERAL | 
         Binary | STRING_LITERAL | booleanLiteral | CHAR_LITERAL | NONE;
booleanLiteral: TRUE | FALSE;
Binary: '0b' [0-1]+;
arrayLiteral: '[' expression (',' expression)* ']' | '[' expression ';' expression ']';
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
