grammar repeat_arr;

// ---------------- PARSER RULES ----------------

program
    : varDecl+ functionDecl+ EOF
    ;

varDecl
    : LOCAL varList
    | GLOBAL varList
    ;

functionDecl
    : FN INTEGER LPAREN paramList? RPAREN stmt+
    ;

paramList
    : varList
    ;

varList
    : var (COMMA var)*
    ;

stmt
    : call
    | assign
    | ret
    | REPEAT
    ;

call
    : CALL expr LPAREN argList? RPAREN
    ;

argList
    : arg (COMMA arg)*
    ;

arg
    : REF var
    | var
    ;

assign
    : var (LBRACK expr RBRACK)? ASSIGN expr
    ;

ret
    : (IF expr)? RETURN
    ;

expr
    : expr (EQ|LE|LT|NEQ|GE|GT) expr     # ComparisonExpr
    | expr (AND|OR) expr                 # LogicalExpr
    | expr (PLUS|MINUS) expr             # ArithExpr
    | expr (IMPL|EQUIV) expr             # ConnExpr
    | atom                               # AtomExpr
    ;

atom
    : INTEGER               # IntAtom
    | TRUE                  # TrueAtom
    | FALSE                 # FalseAtom
    | var                   # VarAtom
    | var LBRACK expr RBRACK # IndexAtom
    | LPAREN expr RPAREN    # ParenAtom
    ;

var
    : ID
    | ATFN
    ;

// ---------------- LEXER RULES ----------------

FN      : 'fn';
CALL    : 'call';
IF      : 'if';
RETURN  : 'return';
REF     : 'ref';
REPEAT  : 'repeat';
LOCAL   : 'local';
GLOBAL  : 'global';

TRUE    : 'TRUE';
FALSE   : 'FALSE';

LE: '<=';
EQ: '==';
LT: '<';
NEQ: '!=';
GE: '>=';
GT: '>';
AND: '&';
OR: '|';
IMPL: '=>';
EQUIV: '<=>';
ASSIGN  : '=';
PLUS    : '+';
MINUS   : '-';
COMMA   : ',';

LPAREN  : '(';
RPAREN  : ')';
LBRACK  : '[';
RBRACK  : ']';

INTEGER : '-'?[0-9]+;
ID      : [a-z]+;
ATFN    : '@fn';

WS      : [ \t\r\n]+ -> skip;
