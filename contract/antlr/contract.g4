grammar contract;

// ---------------- PARSER RULES ----------------

init : contract EOF;
contract
    : LPAREN contract RPAREN
    | (EXISTS|FORALL) VAR COLON LPAREN contract RPAREN
    | contract (EQ|LE|LT|NEQ|GE|GT) contract
    | NOT contract
    | contract (AND|OR) contract
    | contract (IMPL|EQUIV) contract
    | LBRACKET trace RBRACKET LPAREN contract RPAREN
    | LDIAMOND trace RDIAMOND LPAREN contract RPAREN
    | contract_atom
    ;

trace
    : LPAREN trace RPAREN KLEENE
    | LPAREN trace CUP trace RPAREN
    | trace DOT trace
    | trace_atom
    ;

contract_atom
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