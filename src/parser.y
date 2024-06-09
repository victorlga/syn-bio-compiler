%{
#include <stdio.h>

extern FILE *yyin;

void yyerror(const char *s);
int yylex(void);
%}

%union {
    int num;
    char* str;
}

%token <num> NUMBER
%token <str> STRING

%token CREATE WITH NAME IT OF COMMA PERIOD OR AND PLUS MINUS 
%token IF WHILE NOT LESS THAN GREATER EQUAL TO IS LPAREN
%token SALARY COMPANY ROLE FUND PORTFOLIO SIZE STRATEGY CASH
%token REVENUE EXPENSES PRODUCT STARTUP VENTURE WORKER RPAREN
%token SHOWS IDENTIFIER DIFFERENT HAS FIRM STAR SLASH TEAM

%%

program:
    statements
    ;

statements:
    statement PERIOD statements
    | /* empty */
    ;

comma_statements:
    statement COMMA comma_statements
    | statement PERIOD
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
    CREATE entity WITH NAME IDENTIFIER
    ;

assignment:
    IDENTIFIER parameter IS bool_expression
    ;

print_statement:
    IDENTIFIER SHOWS bool_expression
    ;

while_statement:
    WHILE bool_expression COMMA comma_statements
    ;

if_statement:
    IF bool_expression COMMA comma_statements
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
    LESS THAN
    | GREATER THAN
    | EQUAL TO
    | DIFFERENT TO
    ;

expression:
    term
    | term PLUS expression
    | term MINUS expression
    ;

term:
    factor
    | factor STAR term
    | factor SLASH term
    ;

factor:
    NUMBER
    | STRING
    | IDENTIFIER parameter
    | LPAREN expression RPAREN
    | NOT factor
    | PLUS factor
    | MINUS factor
    ;

entity:
    STARTUP
    | VENTURE FIRM
    | WORKER
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
    | TEAM
    ;

venture_parameter:
    PORTFOLIO SIZE
    | STRATEGY
    | FUND
    ;

worker_parameter:
    SALARY
    | COMPANY
    | ROLE
    ;

%%

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Expected args: %s <input_file>\n", argv[0]);
        return 1;
    }
    FILE *input_file = fopen(argv[1], "r");
    if (!input_file) {
        fprintf(stderr, "Error: could not open file %s\n", argv[1]);
        return 1;
    }
    yyin = input_file;
    yyparse();

    fclose(input_file);
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "error: %s\n", s);
}
