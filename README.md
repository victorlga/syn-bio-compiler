# Zombie Startup Compiler

At the time of writing this, I had a total of one year's professional experience as an intern. I had already seen three layoffs and one company completely shut down its operations in Brazil. These are crazy times for tech dudes.

As a parody, I'm going to build a programming language capable of simulating the finances in the life cycle of a startup. Anyone who can type on a computer can simulate a company's decisions (check design principle #1) and see if it survives or dies.

## Design Principles
1. Absolutly everyone should be able to code and write Zombie Startup Script. Need to feel almost like plain text. Why? Raising venture dollars to burn it all until the end of the year is already stressful enough. No time to learn stupid code sintax, simulating a startup should be pretty straightforward.
2. Principles don't raise venture dollars. #1 is enough.

## Language Grammar Description (EBNF)

Not having else was intentional. Else statements make my code ugly.

```
BLOCK = { INLINE_STATEMENT };
INLINE_STATEMENT = STATEMENT, ".";
STATEMENT = ( λ | VARDEC | ASSIGNMENT | PRINT | WHILE | IF );
VARDEC = "create", ENTITY, "with name", IDENTIFIER;
ASSIGNMENT = IDENTIFIER, PARAMETER, "is", BOOL_EXPRESSION;
PRINT = IDENTIFIER, "shows", BOOL_EXPRESSION;
WHILE = "while", BOOL_EXPRESSION, ",", STATEMENT, { ",", STATEMENT };
IF = "if", BOOL_EXPRESSION, ",", STATEMENT, { ",", STATEMENT };
BOOL_EXPRESSION = BOOL_TERM, { "or", BOOL_TERM };
BOOL_TERM = RELATIONAL_EXPRESSION, { "and", RELATIONAL_EXPRESSION };
RELATIONAL_EXPRESSION = EXPRESSION, { ( "less than"  | "greater than" | "equal to" | "different to" ), EXPRESSION };
EXPRESSION = TERM, { ( "+" | "-" ), TERM };
TERM = FACTOR, { ( "*" | "/" ), FACTOR };
FACTOR = ( NUMBER | STRING | IDENTIFIER, ( PARAMETER | λ ) | "(", EXPRESSION, ")" | ( "+" | "-" | "not" ), FACTOR ); 
ENTITY = ( "startup" | "venture firm" | "worker" | IDENTIFIER );
PARAMETER = ( STARTUP_PARAMETER | VENTURE_PARAMETER | WORKER_PARAMETER );
STARTUP_PARAMETER = ( "cash" | "revenue" | "expenses" | "product" | "team" );
VENTURE_PARAMETER = ( "fund" | "portfolio_size" | "strategy" );
WORKER_PARAMETER = ( "salary" | "company" | "role" );
IDENTIFIER = LETTER, { LETTER | DIGIT | " " };
NUMBER = DIGIT, { DIGIT };
DIGIT = ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 );
LETTER = CHAR;
```

## Code Example

```
create startup with name blob.

blob cash is 100000.
blob revenue is 10000.
blob expenses is 15000.
blob product is "some useless OpenAI wrapper".
blob team is 5.
while blob cash greater than 0, blob expenses is 90000.

create venture firm with name daddy.
daddy fund is 100000000.
daddy portfolio_size is 3.
daddy strategy is "spray and pray".

blob asks daddy to raise 1000000.

create worker with name enzo.
enzo salary is 40000.
enzo company is "FAANG".
enzo role is "product manager".

blob hires enzo.

while blob cash less than 0,
blob revenue is 5000,
blob expenses is 10000,
daddy shows "Blob is going to die, hire more FAANG workers!!!".

if blob team greater than 0, blob layoffs.
blob dies.

daddy shows "What? I have never invested in blob. He is crazy for posting that on X".
```