grammar TypeLang;


 // Grammar of this Programming Language
 //  - grammar rules start with lowercase

 program returns [Program ast]        
        locals [ArrayList<DefineDecl> defs, Exp expr]
        @init { $defs = new ArrayList<DefineDecl>(); $expr = new UnitExp(); } :
        (def=definedecl { $defs.add($def.ast); } )* (e=exp { $expr = $e.ast; } )? 
        { $ast = new Program($defs, $expr); }
        ;
 
exp returns [Exp ast]: 
        va=varexp { $ast = $va.ast; }
        | num=numexp { $ast = $num.ast; }
        | str=strexp { $ast = $str.ast; }
        | bl=boolexp { $ast = $bl.ast; }
        | add=addexp { $ast = $add.ast; }
        | sub=subexp { $ast = $sub.ast; }
        | mul=multexp { $ast = $mul.ast; }
        | div=divexp { $ast = $div.ast; }
        | let=letexp { $ast = $let.ast; }
        | lam=lambdaexp { $ast = $lam.ast; }
        | call=callexp { $ast = $call.ast; }
        | i=ifexp { $ast = $i.ast; }
        | sw=switchexp { $ast = $sw.ast; }
        | less=lessexp { $ast = $less.ast; }
        | eq=equalexp { $ast = $eq.ast; }
        | gt=greaterexp { $ast = $gt.ast; }
        | car=carexp { $ast = $car.ast; }
        | cdr=cdrexp { $ast = $cdr.ast; }
        | cons=consexp { $ast = $cons.ast; }
        | list=listexp { $ast = $list.ast; }
        | nl=nullexp { $ast = $nl.ast; }
        | ref=refexp { $ast = $ref.ast; }
        | deref=derefexp { $ast = $deref.ast; }
        | assign=assignexp { $ast = $assign.ast; }
        | free=freeexp { $ast = $free.ast; }
        ;
 

 numexp returns [NumExp ast]:
        n0=Number { $ast = new NumExp(Integer.parseInt($n0.text)); } 
        | '-' n0=Number { $ast = new NumExp(-Integer.parseInt($n0.text)); }
        | n0=Number Dot n1=Number { $ast = new NumExp(Double.parseDouble($n0.text+"."+$n1.text)); }
        | '-' n0=Number Dot n1=Number { $ast = new NumExp(Double.parseDouble("-" + $n0.text+"."+$n1.text)); }
        ;       
  
 addexp returns [AddExp ast]
        locals [ArrayList<Exp> list]
        @init { $list = new ArrayList<Exp>(); } :
        '(' '+'
            e=exp { $list.add($e.ast); } 
            ( e=exp { $list.add($e.ast); } )+
        ')' { $ast = new AddExp($list); }
        ;
 
 subexp returns [SubExp ast]  
        locals [ArrayList<Exp> list]
        @init { $list = new ArrayList<Exp>(); } :
        '(' '-'
            e=exp { $list.add($e.ast); } 
            ( e=exp { $list.add($e.ast); } )+ 
        ')' { $ast = new SubExp($list); }
        ;

 multexp returns [MultExp ast] 
        locals [ArrayList<Exp> list]
        @init { $list = new ArrayList<Exp>(); } :
        '(' '*'
            e=exp { $list.add($e.ast); } 
            ( e=exp { $list.add($e.ast); } )+ 
        ')' { $ast = new MultExp($list); }
        ;
 
 divexp returns [DivExp ast] 
        locals [ArrayList<Exp> list]
        @init { $list = new ArrayList<Exp>(); } :
        '(' '/'
            e=exp { $list.add($e.ast); } 
            ( e=exp { $list.add($e.ast); } )+ 
        ')' { $ast = new DivExp($list); }
        ;

 varexp returns [VarExp ast]: 
        id=Identifier { $ast = new VarExp($id.text); }
        ;

 letexp  returns [LetExp ast] 
        locals [ArrayList<String> names, ArrayList<Type> types, ArrayList<Exp> value_exps]
        @init { $names = new ArrayList<String>(); $types=new ArrayList<Type>(); $value_exps = new ArrayList<Exp>(); } :
        '(' Let 
            '(' ( '(' id=Identifier ':' t=type e=exp ')' { $names.add($id.text);$types.add($t.ast); $value_exps.add($e.ast); } )+  ')'
            body=exp 
            ')' { $ast = new LetExp($names, $types, $value_exps, $body.ast); }
;


 definedecl returns [DefineDecl ast] :
        '(' Define 
            id=Identifier':' t=type
            e=exp
            ')' { $ast = new DefineDecl($id.text, $t.ast, $e.ast); }
        ;
        

 carexp returns [CarExp ast] :
        '(' Car 
            e=exp 
        ')' { $ast = new CarExp($e.ast); }
        ;

 cdrexp returns [CdrExp ast] :
        '(' Cdr 
            e=exp 
        ')' { $ast = new CdrExp($e.ast); }
        ;

 consexp returns [ConsExp ast] :
        '(' Cons 
            e1=exp 
            e2=exp 
        ')' { $ast = new ConsExp($e1.ast,$e2.ast); }
        ;


 listexp returns [ListExp ast] 
        locals [ArrayList<Exp> list]
        @init { $list = new ArrayList<Exp>(); } :
        '(' List ':' t=type
            ( e=exp { $list.add($e.ast); } )* 
        ')' { $ast = new ListExp($t.ast ,$list); }
        ;

 nullexp returns [NullExp ast] :
        '(' Null 
            e=exp 
        ')' { $ast = new NullExp($e.ast); }
        ;
 
 strexp returns [StrExp ast] :
        s=StrLiteral { $ast = new StrExp($s.text); } 
        ;

 boolexp returns [BoolExp ast] :
        TrueLiteral { $ast = new BoolExp(true); } 
        | FalseLiteral { $ast = new BoolExp(false); } 
        ;



  lambdaexp returns [LambdaExp ast] 
        locals [ArrayList<String> formals, ArrayList<Type> types  ]
        @init { $formals = new ArrayList<String>(); $types = new ArrayList<Type>(); } :
        '(' Lambda 
            '(' (id=Identifier ':' ty=type { $formals.add($id.text); $types.add($ty.ast); } )* ')'
            body=exp
        ')' {$ast = new LambdaExp($formals, $types, $body.ast); }
        ;

 callexp returns [CallExp ast] 
        locals [ArrayList<Exp> arguments = new ArrayList<Exp>();  ] :
        '(' f=exp 
            ( e=exp { $arguments.add($e.ast); } )* 
        ')' { $ast = new CallExp($f.ast,$arguments); }
        ;

 ifexp returns [IfExp ast] :
        '(' If 
            e1=exp 
            e2=exp 
            e3=exp 
        ')' { $ast = new IfExp($e1.ast,$e2.ast,$e3.ast); }
        ;


 switchexp returns [SwitchExp ast]
         locals [ArrayList<Exp> cases = new ArrayList<Exp>();, ArrayList<Exp> body = new ArrayList<Exp>();] :
  		'(' Switch
  			'(' e0=exp ')'
  			 ('(' 'case' e1=exp  e2=exp  { $cases.add($e1.ast); $body.add($e2.ast);  } ')' )+
  			'(' ('default' e3=exp) ')'
  		')' { $ast = new SwitchExp($e0.ast, $cases, $body, $e3.ast); }
  		;



 lessexp returns [LessExp ast] :
        '(' Less 
            e1=exp 
            e2=exp 
        ')' { $ast = new LessExp($e1.ast,$e2.ast); }
        ;

 equalexp returns [EqualExp ast] :
        '(' Equal 
            e1=exp 
            e2=exp 
        ')' { $ast = new EqualExp($e1.ast,$e2.ast); }
        ;

 greaterexp returns [GreaterExp ast] :
        '(' Greater 
            e1=exp 
            e2=exp 
        ')' { $ast = new GreaterExp($e1.ast,$e2.ast); }
        ;


 refexp returns [RefExp ast] :
        '(' Ref ':' t=type
            e=exp
        ')' { $ast = new RefExp($e.ast, $t.ast); }
        ;

 derefexp returns [DerefExp ast] :
        '(' Deref
            e=exp
        ')' { $ast = new DerefExp($e.ast); }
        ;

 assignexp returns [AssignExp ast] :
        '(' Assign
            e1=exp
            e2=exp
        ')' { $ast = new AssignExp($e1.ast, $e2.ast); }
        ;

 freeexp returns [FreeExp ast] :
        '(' Free
            e=exp
         ')' { $ast = new FreeExp($e.ast); }
        ;


type returns [Type ast]: 
        b=booleantype { $ast = $b.ast; }
        |f=funct  { $ast = $f.ast; }
        |n=numtype { $ast = $n.ast; }
        |l=listtype { $ast = $l.ast; }
        |p=pairtype { $ast = $p.ast; }
        |s=stringt { $ast = $s.ast; }
        |r=reft { $ast = $r.ast; }
        |u=unittype { $ast = $u.ast; }
        ;

booleantype returns [BoolT ast] :
        'bool' { $ast = new BoolT(); }
        ;

unittype returns [UnitT ast] :
        'unit' { $ast = new UnitT(); }
        ;

numtype returns [NumT ast] :
        'num' { $ast = new NumT(); }
        ;

listtype returns [ListT ast] :
        'List<' ret = type '>' { $ast = new ListT($ret.ast); }
        ;
        
pairtype returns [PairT ast] :
        '(' fst = type ',' snd= type ')' { $ast = new PairT($fst.ast, $snd.ast); }
        ;
        
reft returns [RefT ast] :
        'Ref' ret = type  { $ast = new RefT($ret.ast); }
        ;
        
stringt returns [StringT ast] :
         'Str'{  $ast = new StringT(); }
        ;

 funct returns [FuncT ast] 
        locals [ArrayList<Type> formals]
        @init { $formals = new ArrayList<Type>(); } :
        '('  
             (e=type { $formals.add($e.ast);} )* '->' ret=type 
        ')' { $ast = new FuncT($formals, $ret.ast); }
        ;




 // Lexical Specification of this Programming Language
 //  - lexical specification rules start with uppercase
 
 Define : 'define' ;
 Let : 'let' ;
 Lambda : 'lambda' ;
 If : 'if' ;
 Switch : 'switch' ;
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
 Ref : 'ref' ;
 Deref : 'deref' ;
 Assign : 'set' ;
 Free : 'free' ;
 Fork : 'fork' ;
 Lock : 'lock' ;
 UnLock : 'unlock' ;
 Process : 'process' ;
 Send : 'send' ;
 Stop : 'stop' ;
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
