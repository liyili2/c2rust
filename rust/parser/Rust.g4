grammar Rust;

program: (topLevelItem)* ;

topLevelItem
    : topLevelDef
    | staticVarDecl
    | attributes
    | externBlock
    | useDecl
    | typeAlias;

useDecl: 'use' typePath ('{' (typePath? (Identifier | '{' (Identifier ','?)* '}') ','? )* '}' ',' )* ';';
topLevelDef: functionDef | structDef | interfaceDef | topLevelVarDef;
topLevelVarDef: visibility? defKind? Identifier  ((':' typeExpression '=' expression ';') | '{' varDefField* '}');
staticVarDecl: visibility? 'static'? 'mut'? Identifier ':' (typeExpression | Identifier) '=' initializer ';';
defKind: 'const' | 'union' | 'unsafe';
varDefField: visibility? Identifier ':' typeExpression ','?;

typeAlias: visibility? 'type' Identifier '=' typeExpression ';';
interfaceDef: 'impl' Identifier '{' functionDef+ '}' ;

externBlock: 'extern' STRING_LITERAL '{' externItem* '}';
externItem
    : visibility? 'type' Identifier ';'
    | visibility? 'static' 'mut'? Identifier ':' typeExpression ';'
    | visibility? 'fn' Identifier '(' externParams? ')' 
        ('->' typeExpression)? ';';
externParams: externParam (',' externParam)* (',' '...')? | '...';
externParam: (UNDERSCORE | Identifier)? ':' (typeExpression | ELLIPSIS);

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
structField: visibility? Identifier ':' typeExpression ','?;
structLiteral: Identifier '{' structLiteralField* '}' ;
structLiteralField: Identifier (':' expression)? ','? ;

functionDef: visibility? unsafeModifier? externAbi? 'fn' Identifier ('()' | '(' paramList? ')') '->'? typeExpression? block;
paramList: param (',' param)* (',')?;
param: '&'? 'mut'? Identifier (':' typeExpression)?;

typePath: Identifier (DOUBLE_COLON Identifier)* ;

typeExpression: basicType | pointerType;
basicType
    : scalarType
    | stdLibraryType
    | safeNonNullWrapper
    | arrayType
    | pathType
    | genericType
    | referenceType
    | sliceType
    | unitType
    | Identifier;
pointerType: '*' (MUT | CONST) (typeExpression)?;
scalarType: intType | floatingPointType | boolType | charType;
intType: signedIntType | unsignedIntType;
signedIntType: 'i8' | 'i16' | 'i32' | 'i64' | 'i128';
unsignedIntType: 'u8' | 'u16' | 'u32' | 'u64' | 'u128';
floatingPointType: 'f32' | 'f64';
boolType: 'bool';
charType: 'char';
stdLibraryType: stringType;
stringType: 'String';
safeNonNullWrapper: 'Option<NonNull<' typeExpression ('>>' | '>' '>') ;
arrayType: '[' basicType ';' Number ']' ;
pathType: typePath basicType;
genericType: typePath? '<' typeExpression (',' typeExpression)* '>';
referenceType: '&' typeExpression;
sliceType: '[' typeExpression ']';
unitType: '()';

block: unsafeModifier? '{' statement* returnStmt? '}';
statement
    : block
    | letStmt
    | conditionalAssignmentStmt
    | structLiteral
    | structDef
    | staticVarDecl
    | safeWrapper
    | assignStmt
    | compoundAssignment
    | forStmt
    | ifStmt 
    | functionCall
    | exprStmt
    | whileStmt
    | returnStmt
    | loopStmt
    | 'break' ';'
    | 'continue' ';'
    | matchStmt
    ;

conditionalAssignmentStmt: 'let'? (safeWrapper | expression) '=' expression 'else' block ';';
functionCall: expression ('.' expression)? callExpressionPostFix ';';
letStmt: 'let' varDef '=' expression ';' | 'let' varDef initBlock | 'let' '(' (varDef ','?)* ')' '=' '(' (expression ','?)* ')' ';';
varDef: 'ref'? 'mut'? Identifier (':' typeExpression)?;
compoundOp: '+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' ;
compoundAssignment: expression compoundOp expression ';' ;
matchStmt: 'match' expression '{' matchArm+ '}' ;
matchArm: matchPattern ('|' matchPattern)* '=>' (block | 'return' (expression)?);
matchPattern: byteLiteral | Number | UNDERSCORE | Identifier;
whileStmt: 'while' expression block;
initializer: initBlock | block | expression ;
initBlock: '{' (Identifier ':' expression ',')* '}' ';' expression;
assignStmt: expression '=' expression ';';
forStmt: 'for' Identifier 'in' expression block;
ifStmt: 'if' expression block ('else if' expression block)* ('else' block)?;
exprStmt: primaryExpression ';';
returnStmt: 'return' (expression | statement)? (';')? | Identifier;
loopStmt: 'loop' block;

safeWrapper: 'Some' '(' expression ')' | 'Some' '(' 'ref'? 'mut'? expression ')' | 'Box' DOUBLE_COLON Identifier '(' expression ')' ;

expression
    : MUT expression
    | arrayAccess
    | expression callExpressionPostFix
    | expression fieldAccessPostFix
    | safeWrapper
    | primaryExpression
    | expression binaryOps expression
    | structLiteral
    | expression castExpressionPostFix
    | typePathExpression expression
    | parenExpression
    | structFieldDec
    | structDefInit
    | unaryOpes expression
    | borrowExpression
    | unsafeModifier parenExpression
    | expression typeExpression
    | expression rangeSymbol expression
    | dereferenceExpression
    | expression compoundOps expression
    | expressionBlock
    | qualifiedExpression
    | patternPrefix expression
    | arrayDeclaration
    ;

unsafeExpression: 'unsafe' '{' expression '}' ;
qualifiedExpression: '<' expression '>';
structDefInit: Identifier '=' '{' expression '}' ';' ;
arrayDeclaration: Identifier '!'? '[' Number ';' expression ']' ;
typePathExpression: (Identifier DOUBLE_COLON)+ ;
patternPrefix: 'let'? pattern '=' ;
pattern: safeWrapper | 'ref'? 'mut'? Identifier;
castExpressionPostFix: 'as' typeExpression ('as' typeExpression)*;
compoundOps: '+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=';
rangeSymbol: '..';

binaryOps: '*' | '/' | '%' | '+' | '-' | '==' | '!=' | '>' | '<' | '||' | '&&' | '>>' | '&' | '>=' | '<=';
structFieldDec: Identifier '{' structLiteralField (',' structLiteralField)* ','? '}' ;
unaryOpes: '!' | '+' | '-';
parenExpression: '(' expression ')' | '{' expression '}';
dereferenceExpression: '*' expression;
expressionBlock: '{' statement* expression '}';
borrowExpression: '&' expression;
primaryExpression: literal | Identifier;

fieldAccessPostFix: ('.' primaryExpression)+ | '[' primaryExpression ']';
callExpressionPostFix: '!'? functionCallArgs;
functionCallArgs: '()' | '(' expression (',' expression)* ')' ;

TRUE: 'true';
FALSE: 'false';
NONE: 'None';
literal: arrayLiteral | HexNumber | Number | SignedNumber | BYTE_STRING_LITERAL | 
         Binary | STRING_LITERAL | booleanLiteral | CHAR_LITERAL | byteLiteral |  NONE;
byteLiteral: 'b\'.\'' | 'b\'|\'' | 'b\'*\'' | 'b\'' LPAREN '\'' | 'b\'' RPAREN '\'' | 'b\'+\'' | 'b\'?\'';

MUT: 'mut';
CONST: 'const';

booleanLiteral: TRUE | FALSE;
Binary: '0b' [0-1]+;
arrayAccess: Identifier '[' expression ']';
arrayLiteral: Identifier? '!'? '[' expression (',' expression)+ ']' | Identifier? '!'? '[' expression ';' expression ']' | Identifier? '!'? '[' ']';
STRING_LITERAL: '"' (~["\\] | '\\' .)* '"';
stringLiteral: '"' .*? '"';
Identifier: [a-zA-Z_][a-zA-Z0-9_]*;
Number: [0-9]+;
SignedNumber: ('-' | '+') Number;
BYTE_STRING_LITERAL: 'b"' (~["\\\r\n] | '\\' .)* '"';
HexNumber: '0x' [0-9a-fA-F]+;
CHAR_LITERAL: '\'' (~['\\\r\n] | '\\') '\'';
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