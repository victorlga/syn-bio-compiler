# Zombie Startup Compiler

At the time of writing this, I had a total of one year's professional experience as an intern. I had already seen three layoffs and one company completely shut down its operations in Brazil. These are crazy times for tech dudes.

As a parody, I'm going to build a programming language capable of simulating the finances in the life cycle of a startup. Anyone who can type on a computer can simulate a company's decisions and see if it survives or dies.

## Language Grammar Description (EBNF)

Not having else was intentional. Else statements make my code ugly.

```
BLOCK = { INLINE_STATEMENT };
INLINE_STATEMENT = STATEMENT, ".";
STATEMENT = ( λ | VARDEC | ASSIGNMENT | PRINT | WHILE | IF | STARTUP_FUNCTION );
VARDEC = "create", ENTITY, "with name", IDENTIFIER, { ",", "it has", TYPE, "of", IDENTIFIER };
ASSIGNMENT = IDENTIFIER, ( PARAMETER | λ ), "is", BOOL_EXPRESSION;
PRINT = IDENTIFIER, "shows", ( PARAMETER | BOOL_EXPRESSION );
WHILE = "while", BOOL_EXPRESSION, ",", STATEMENT, { ",", STATEMENT };
IF = "if", BOOL_EXPRESSION, ",", STATEMENT, { ",", STATEMENT };
STARTUP_FUNCTION = IDENTIFIER, (
    "hires", IDENTIFIER | 
    "layoffs" |
    "asks", IDENTIFIER, "to raise", NUMBER, ",", IDENTIFIER, ( "not" | λ ), "throws money" |
    "dies" |
    PARAMETER, ( "increases" | "decreases" ), BOOL_EXPRESSION
);
BOOL_EXPRESSION = BOOL_TERM, { "or", BOOL_TERM };
BOOL_TERM = RELATIONAL_EXPRESSION, { "and", RELATIONAL_EXPRESSION };
RELATIONAL_EXPRESSION = EXPRESSION, { "is", ( "not" | λ ), ( "less than"  | "greater than" | "equal to" ), EXPRESSION };
EXPRESSION = TERM, { ( "+" | "-" ), TERM };
TERM = FACTOR, { ( "*" | "/" ), FACTOR };
FACTOR = ( NUMBER | STRING | IDENTIFIER, ( PARAMETER | λ ) | "(", EXPRESSION, ")" | ( "+" | "-" | "not" ), FACTOR ); 
ENTITY = ( "startup" | "venture firm" | "worker" );
PARAMETER = ( STARTUP_PARAMETER | VENTURE_PARAMETER | WORKER_PARAMETER | IDENTIFIER );
STARTUP_PARAMETER = ( "cash" | "monthly revenue" | "monthly expenses" | "product" );
VENTURE_PARAMETER = ( "fund" | "portfolio size" | "investment strategy" );
WORKER_PARAMETER = ( "salary" | "company" | "role" );
TYPE = ( "number" | "text" | "belief" );
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" };
NUMBER = DIGIT, { DIGIT };
DIGIT = ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 );
LETTER = CHAR;
```

## Code Example

```
create startup with name blob,
it has number of founders team size.

blob cash is 100000.
blob monthly revenue is 10000.
blob monthly expenses is 15000.
blob product is "some useless OpenAI wrapper".
blob founders team size is 3.

while blob cash is not less than 0,
blob monthly expenses increases 10000.

create venture firm with name daddy.
daddy fund is 100000000.
daddy portfolio size is 3.
daddy investment strategy is spray and pray.

blob asks daddy to raise 1000000, daddy throws money.

create worker with name enzo.
enzo salary is 40000.
enzo company is FAANG.
enzo role is product manager.

blob hires enzo.

while blob cash is not less than 0,
blob monthly revenue increases 5000,
blob monthly expenses increases 10000,
daddy shows "Blob is going to die, hire more FAANG workers!!!".

if blob team is greater than 0,
blob layoffs.
blob dies.

daddy shows "What? I have never invested in blob. He is crazy for posting that on X.".
```