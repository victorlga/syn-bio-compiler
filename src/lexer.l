%{
#include "parser.tab.h"
%}

DIGIT               [0-9]
LETTER              [a-zA-Z]
IDENTIFIER          {LETTER}({LETTER}|{DIGIT}|[ ])*
NUMBER              {DIGIT}+
STRING              \"[^"]*\"
WS                  [ \t\r\n]+

%%

{WS}                    { /* Ignore whitespace */ }
"portfolio size"        { return PORTFOLIO_SIZE; }
"with name"             { return WITH_NAME; }
"strategy"              { return STRATEGY; }
"greater"               { return GREATER; }
"less"                  { return LESS; }
"than"                  { return THAN; }
"equal"                 { return EQUAL; }
"to"                    { return TO; } 
"different"             { return DIFFERENT; }
"revenue"               { return REVENUE; }
"expenses"              { return EXPENSES; }
"venture firm"          { return VENTURE_FIRM; }
"it has"                { return IT_HAS; }
"create"                { return CREATE; }
"if"                    { return IF; }
"while"                 { return WHILE; }
"not"                   { return NOT; }
"is"                    { return IS; }
"salary"                { return SALARY; }
"company"               { return COMPANY; }
"team"                  { return TEAM; }
"role"                  { return ROLE; }
"fund"                  { return FUND; }
"cash"                  { return CASH; }
"product"               { return PRODUCT; }
"startup"               { return STARTUP; }
"worker"                { return WORKER; }
"of"                    { return OF; }
"shows"                 { return SHOWS; }
","                     { return COMMA; }
"."                     { return PERIOD; }
"or"                    { return OR; }
"and"                   { return AND; }
"+"                     { return PLUS; }
"-"                     { return MINUS; }
"*"                     { return STAR; }
"/"                     { return SLASH; }
"("                     { return LPAREN; }
")"                     { return RPAREN; }
{STRING}                { yylval.str = strdup(yytext); return STRING; }
{NUMBER}                { yylval.num = atoi(yytext); return NUMBER; }
{IDENTIFIER}            { yylval.str = strdup(yytext); return IDENTIFIER; }

%%

int yywrap() {
    return 1;
}
