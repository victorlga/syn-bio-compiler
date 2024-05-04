%{
#include "parser.tab.h"

typedef union {
    int num;           // For numeric values
    char *str;         // For string values
} YYSTYPE;

YYSTYPE yylval;

%}

DIGIT       [0-9]
LETTER      [a-zA-Z]
IDENTIFIER  {LETTER}({LETTER}|{DIGIT}|[ ])*
NUMBER      {DIGIT}+
STRING      \"[^"]*\"
WS          [ \t\r\n]+

%%

{WS}                    { /* Ignore whitespace */ }
"portfolio size"        { return PORTFOLIO_SIZE; }
"with name"             { return WITH_NAME; }
"investment strategy"   { return INVESTMENT_STRATEGY; }
"greater than"          { return GREATER_THAN; }
"less than"             { return LESS_THAN; }
"equal to"              { return EQUAL_TO; }
"monthly revenue"       { return MONTHLY_REVENUE; }
"monthly expenses"      { return MONTHLY_EXPENSES; }
"venture firm"          { return VENTURE_FIRM; }
"to raise"              { return TO_RAISE; }
"throws money"          { return THROWS_MONEY; }
"it has"                { return IT_HAS; }
"create"                { return CREATE; }
"if"                    { return IF; }
"while"                 { return WHILE; }
"is"                    { return IS; }
"not"                   { return NOT; }
"number"                { return NUMBER_TYPE; }
"text"                  { return TEXT_TYPE; }
"belief"                { return BELIEF_TYPE; }
"salary"                { return SALARY; }
"company"               { return COMPANY; }
"role"                  { return ROLE; }
"fund"                  { return FUND; }
"cash"                  { return CASH; }
"product"               { return PRODUCT; }
"startup"               { return STARTUP; }
"worker"                { return WORKER; }
"hires"                 { return HIRES; }
"layoffs"               { return LAYOFFS; }
"asks"                  { return ASKS; }
"dies"                  { return DIES; }
"increases"             { return INCREASES; }
"decreases"             { return DECREASES; }
"of"                    { return OF; }
"shows"                 { return SHOWS; }
","                     { return COMMA; }
"."                     { return DOT; }
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
