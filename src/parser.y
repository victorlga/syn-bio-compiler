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
%token IF WHILE NOT LESS_THAN GREATER_THAN EQUAL_TO
%token SALARY COMPANY ROLE FUND PORTFOLIO_SIZE STRATEGY CASH
%token REVENUE EXPENSES PRODUCT STARTUP VENTURE_FIRM WORKER
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
    ;

var_declaration:
    CREATE entity WITH_NAME IDENTIFIER
    ;

assignment:
    IDENTIFIER parameter bool_expression
    | IDENTIFIER bool_expression
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
    | expression relational_operator expression
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
    STARTUP | VENTURE_FIRM | WORKER
    ;

parameter:
    startup_parameter
    | venture_parameter
    | worker_parameter
    ;

startup_parameter:
    CASH
    | REVENUE
    | EXPENSES
    | PRODUCT
    ;

venture_parameter:
    PORTFOLIO_SIZE
    | STRATEGY
    | FUND
    ;

worker_parameter:
    SALARY
    | COMPANY
    | ROLE
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
