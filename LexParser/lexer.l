%{
#include <stdio.h>
%}

%%
[ \t]            ; /* Ignora espaços em branco e tabulações */
"if"             { printf("IF\n"); }
"else"           { printf("ELSE\n"); }
"foreach"        { printf("FOREACH\n"); }
"to"             { printf("TO\n"); }
"while"          { printf("WHILE\n"); }
"show"           { printf("SHOW\n"); }
"rule"           { printf("RULE\n"); }
"match"          { printf("MATCH\n"); }
"scanhost"       { printf("SCANHOST\n"); }
"traffic_information" { printf("TRAFFIC_INFORMATION\n"); }
"input"          { printf("INPUT\n"); }
int              { printf("INT\n"); }
str              { printf("STR\n"); }
":"              { printf("DECLARE\n"); }
"("              { printf("LPAREN\n"); }
")"              { printf("RPAREN\n"); }
"{"              { printf("LBRACE\n"); }
"}"              { printf("RBRACE\n"); }
","              { printf("COMMA\n"); }
";"              { printf("SEMICOLON\n"); }
"=="             { printf("EQ\n"); }
">"              { printf("GT\n"); }
"<"              { printf("LT\n"); }
"&&"             { printf("AND\n"); }
"||"             { printf("OR\n"); }
"+"              { printf("PLUS\n"); }
"-"              { printf("MINUS\n"); }
"*"              { printf("TIMES\n"); }
"/"              { printf("DIVIDE\n"); }
"="              { printf("ASSIGN\n"); }
"!"              { printf("NOT\n"); }
[0-9]+           { printf("NUMBER: %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]* { printf("IDENTIFIER: %s\n", yytext); }
\"([^\\\"]|\\.)*\" { printf("STRING: %s\n", yytext); }

"//"(.)*         ; /* Ignora comentários de uma linha */

"\\\n"           ; /* Ignora quebras de linha precedidas por \ */

\n               ; /* Ignora quebras de linha não precedidas por \ */

.               { printf("UNKNOWN CHARACTER: %s\n",yytext); }
%%

int main() {
    yylex();
    return 0;
}
