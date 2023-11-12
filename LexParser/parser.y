%{
#include <stdio.h>
int yylex();
void yyerror(const char *s);
%}

%token IF
%token ELSE
%token FOREACH
%token TO
%token WHILE
%token SHOW
%token RULE
%token MATCH
%token SCANHOST
%token TRAFFIC_INFORMATION
%token INPUT
%token INT
%token STR
%token LPAREN
%token RPAREN
%token LBRACE
%token RBRACE
%token COMMA
%token SEMICOLON
%token EQ
%token GT
%token LT
%token AND
%token OR
%token PLUS
%token MINUS
%token TIMES
%token DIVIDE
%token ASSIGN
%token NOT
%token NUMBER
%token IDENTIFIER
%token STRING
%token NEWLINE
%token DECLARE

%%
program: statement
        | program statement;

block: LBRACE NEWLINE statements RBRACE ;

statements: /* empty */
          | statement
          | statements statement
          ;

statement: /* empty */ 
         | assigment
         | conditional
         | print
         | foreach
         | while
         | var
         | rule
         | traffic
         ;

assigment: IDENTIFIER ASSIGN rexpression  NEWLINE
          |IDENTIFIER ASSIGN rexpression 
          ;

conditional: IF bexpression  block
           | IF bexpression  block NEWLINE
           | IF bexpression block ELSE block NEWLINE
           ;

print: SHOW LPAREN bexpression RPAREN NEWLINE;

foreach: FOREACH assigment TO assigment block NEWLINE;

while: WHILE bexpression block;

var: type DECLARE IDENTIFIER ASSIGN bexpression NEWLINE
   | type DECLARE IDENTIFIER NEWLINE
   | type DECLARE IDENTIFIER ASSIGN bexpression
   | type DECLARE IDENTIFIER 
   ;

rule: RULE DECLARE IDENTIFIER LBRACE NEWLINE var_list RBRACE NEWLINE;

var_list: var COMMA NEWLINE
        | var_list var COMMA NEWLINE
        ;

type: INT
    | STR 
    ;

match: MATCH LPAREN IDENTIFIER COMMA IDENTIFIER RPAREN;

scanhost: SCANHOST LPAREN IDENTIFIER COMMA IDENTIFIER RPAREN;

traffic: TRAFFIC_INFORMATION LPAREN RPAREN NEWLINE;

bexpression: bexpression OR bterm
          | bterm
          ;

bterm: bterm AND rexpression
     | rexpression
     ;

rexpression: rexpression EQ expression
           | rexpression GT expression
           | rexpression LT expression
           | expression 
           ;

expression: expression PLUS term
          | expression MINUS term
          | term
          ;

term: term TIMES factor
    | term DIVIDE factor
    | factor
    ;

factor: PLUS factor
      | MINUS factor
      | NOT factor
      | NUMBER 
      | STRING 
      | LPAREN expression RPAREN
      | IDENTIFIER 
      | match 
      | scanhost
      | INPUT LPAREN RPAREN
      ;

%%

void yyerror(const char *s) {
    extern int yylineno;
    extern char *yytext;

    /* mensagem de erro exibe o símbolo que causou erro e o número da linha */
    printf("\nErro (%s): símbolo \"%s\" (linha %d)\n", s, yytext, yylineno);
}

int main() {
    yyparse();
    return 0;
}
