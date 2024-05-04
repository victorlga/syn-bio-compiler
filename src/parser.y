%{
#include <stdio.h>

void yyerror(const char *s);
int yylex(void);
%}

%union {
    int num;
    char* str;
}

%token <num> NUMBER
%token <str> STRING

%token CREATE WITH_NAME IT_HAS OF COMMA DOT OR AND PLUS MINUS STAR SLASH LPAREN RPAREN
%token IF WHILE IS NOT LESS_THAN GREATER_THAN EQUAL_TO
%token NUMBER_TYPE TEXT_TYPE BELIEF_TYPE
%token SALARY COMPANY ROLE FUND PORTFOLIO_SIZE INVESTMENT_STRATEGY CASH
%token MONTHLY_REVENUE MONTHLY_EXPENSES PRODUCT STARTUP VENTURE_FIRM WORKER
%token HIRES LAYOFFS ASKS TO_RAISE THROWS_MONEY DIES INCREASES DECREASES
%token SHOWS IDENTIFIER

%%

program:
    statements
    ;

statements:
    statement DOT statements
    | /* empty */
    ;

statement:
    var_declaration
    | assignment
    | print_statement
    | while_statement
    | if_statement
    | function_call
    ;

var_declaration:
    CREATE entity WITH_NAME IDENTIFIER it_has_clauses
    ;

it_has_clauses:
    it_has_clause it_has_clauses
    | /* empty */
    ;

it_has_clause:
    COMMA IT_HAS type OF bool_expression
    ;

assignment:
    IDENTIFIER parameter IS bool_expression
    | IDENTIFIER IS bool_expression
    ;

print_statement:
    IDENTIFIER SHOWS bool_expression
    | IDENTIFIER SHOWS parameter
    ;

while_statement:
    WHILE bool_expression COMMA statements
    ;

if_statement:
    IF bool_expression COMMA statements
    ;

function_call:
    IDENTIFIER function_params
    ;

function_params:
    HIRES IDENTIFIER
    | LAYOFFS
    | ASKS IDENTIFIER TO_RAISE NUMBER COMMA IDENTIFIER NOT THROWS_MONEY
    | ASKS IDENTIFIER TO_RAISE NUMBER COMMA IDENTIFIER THROWS_MONEY
    | DIES
    | parameter INCREASES bool_expression
    | parameter DECREASES bool_expression
    ;

bool_expression:
    bool_term
    | bool_term OR bool_expression
    ;

bool_term:
    relational_expression
    | relational_expression AND bool_term
    ;

relational_expression:
    expression
    | expression IS NOT relational_operator expression
    | expression IS relational_operator expression
    ;

relational_operator:
    LESS_THAN
    | GREATER_THAN
    | EQUAL_TO
    ;

expression:
    term
    | term PLUS expression
    | term MINUS expression
    ;

term:
    factor
    | factor '*' term
    | factor '/' term
    ;

factor:
    NUMBER
    | STRING
    | IDENTIFIER parameter
    | IDENTIFIER
    | '(' expression ')'
    | NOT factor
    | PLUS factor
    | MINUS factor
    ;

entity:
    STARTUP | VENTURE_FIRM | WORKER | IDENTIFIER
    ;

parameter:
    startup_parameter
    | venture_parameter
    | worker_parameter
    | IDENTIFIER
    ;

startup_parameter:
    CASH
    | MONTHLY_REVENUE
    | MONTHLY_EXPENSES
    | PRODUCT
    ;

venture_parameter:
    PORTFOLIO_SIZE
    | INVESTMENT_STRATEGY
    | FUND
    ;

worker_parameter:
    SALARY
    | COMPANY
    | ROLE
    ;

type:
    NUMBER_TYPE
    | TEXT_TYPE
    | BELIEF_TYPE
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    if (yyparse() == 0) {
        printf("Parsing complete!\n");
    } else {
        printf("Parsing failed.\n");
    }
    return 0;
}
