%{
#include "parser.tab.h"
%}

DIGIT               [0-9]
LETTER              [a-zA-Z]
IDENTIFIER          {LETTER}({LETTER}|{DIGIT})*
NUMBER              {DIGIT}+
STRING              \"[^"]*\"

%%

"portfolio"             { return PORTFOLIO; }
"size"                  { return SIZE; }
"with"                  { return WITH; }
"name"                  { return NAME; }
"strategy"              { return STRATEGY; }
"greater"               { return GREATER; }
"less"                  { return LESS; }
"than"                  { return THAN; }
"equal"                 { return EQUAL; }
"to"                    { return TO; }
"different"             { return DIFFERENT; }
"revenue"               { return REVENUE; }
"expenses"              { return EXPENSES; }
"venture"               { return VENTURE; }
"firm"                  { return FIRM; }
"it"                    { return IT; }
"has"                   { return HAS; }
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
{NUMBER}                { return NUMBER; }
{STRING}                { return STRING; }
{IDENTIFIER}            { return IDENTIFIER; }
[ \t\r\n]+              { /* Ignore whitespace and new lines */ }
.                       { /* Ignore any other single character */ }

%%
