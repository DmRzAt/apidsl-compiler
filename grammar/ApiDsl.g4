grammar ApiDsl;

program   : base? test+ EOF ;
base      : BASE STRING SEMI ;
test      : TEST STRING LBRACE statement* RBRACE ;
statement : request | assertion | save ;
request   : method expr (BODY object)? header* SEMI ;
method    : GET | POST | PUT | DELETE ;
header    : HEADER STRING ASSIGN expr ;
assertion : EXPECT (STATUS NUMBER | JSON STRING EQ value) SEMI ;
save      : SAVE IDENT ASSIGN JSON STRING SEMI ;
expr      : term (PLUS term)* ;
term      : STRING | IDENT ;
object    : LBRACE (pair (COMMA pair)*)? RBRACE ;
pair      : STRING COLON value ;
value     : STRING | NUMBER | IDENT | object | TRUE | FALSE | NULL ;

TEST   : 'TEST' ;
BASE   : 'BASE' ;
GET    : 'GET' ;
POST   : 'POST' ;
PUT    : 'PUT' ;
DELETE : 'DELETE' ;
EXPECT : 'EXPECT' ;
STATUS : 'STATUS' ;
JSON   : 'JSON' ;
SAVE   : 'SAVE' ;
BODY   : 'BODY' ;
HEADER : 'HEADER' ;
TRUE   : 'true' ;
FALSE  : 'false' ;
NULL   : 'null' ;

IDENT  : [a-zA-Z_] [a-zA-Z0-9_]* ;
NUMBER : '-'? [0-9]+ ;
STRING : '"' STRING_CHAR* '"' ;
UNTERMINATED_STRING : '"' STRING_CHAR* '\\'? ;

LBRACE : '{' ;
RBRACE : '}' ;
SEMI   : ';' ;
COLON  : ':' ;
COMMA  : ',' ;
PLUS   : '+' ;
EQ     : '==' ;
ASSIGN : '=' ;

COMMENT : '#' ~[\r\n]* -> skip ;
WS      : [ \t\r\n]+ -> skip ;

fragment STRING_CHAR : '\\' ~[\r\n] | ~["\\\r\n] ;
