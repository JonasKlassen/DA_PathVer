grammar property;

// ---------------- PARSER RULES ----------------

init : property EOF;
property
    : LPAREN property RPAREN
    | (EXISTS|FORALL) VAR COLON LPAREN property RPAREN
    | property (EQ|LE|LT|NEQ|GE|GT) property
    | NOT property
    | property (AND|OR) property
    | property (IMPL|EQUIV) property
    | LBRACKET trace RBRACKET LPAREN property RPAREN
    | LDIAMOND trace RDIAMOND LPAREN property RPAREN
    | property_atom
    ;

trace
    : LPAREN trace RPAREN KLEENE
    | LPAREN trace CUP trace RPAREN
    | trace DOT trace
    | trace_atom
    ;

property_atom
    : VAR
    | indexed_var
    | ATFN
    | INT
    ;

indexed_var
    : VAR LBRACKET (INT|VAR) RBRACKET
    ;

trace_atom
    : WILDCARD
    | DOLLAR
    | HASHTAG
    | INT
    | EPSILON
    ;

// ---------------- LEXER RULES ----------------

LBRACKET: '[';
RBRACKET: ']';
LDIAMOND: '{';
RDIAMOND: '}';
LPAREN: '(';
RPAREN: ')';
NOT: '!';
AND: '&';
OR: '|';
IMPL: '=>';
EQUIV: '<=>';
CUP: 'U';
LE: '<=';
EQ: '==';
LT: '<';
NEQ: '!=';
GE: '>=';
GT: '>';
DOT: '.';
KLEENE: '*';
WILDCARD: '?';
DOLLAR: '$';
HASHTAG: '#';
EPSILON: 'eps';
ATFN: '@fn';
INT: '-'?[0-9]+;
VAR: [a-z]+;
COLON: ':';
EXISTS: 'EXISTS';
FORALL: 'FORALL';

WS: [ \t\r\n]+ -> skip;
