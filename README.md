# Zombie Startup Interpreter

At the time of writing this, I had a total of one year's professional experience as an intern. I had already seen three layoffs and one company completely shut down its operations in Brazil. These are crazy times for tech dudes.

As a parody, I built a programming language capable of simulating the finances in the life cycle of a startup. Anyone who can type on a computer can simulate a company's decisions (check design principle #1) and see if it survives or dies.

## Design Principles
1. Absolutely everyone should be able to code and write Zombie Startup Script. Need to feel almost like plain text. Why? Raising venture dollars to burn it all until the end of the year is already stressful enough. No time to learn stupid code sintax, simulating a startup should be pretty straightforward.
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

blob cash is 200000.
blob revenue is 10000.
blob expenses is 15000.
blob product is "some useless OpenAI wrapper".
blob team is 5.

while blob cash greater than 100000,
blob expenses is blob expenses * 2, blob cash is blob cash - blob expenses + blob revenue,
blob shows "Let's grow without caring about revenue, burn it all!".

create venture firm with name daddy.
daddy fund is 100000000. daddy portfolio_size is 3. daddy strategy is "spray and pray".

if daddy strategy different to "spray and pray",
daddy shows "I invest to generate shareholder value".

if daddy strategy equal to "spray and pray" and daddy portfolio_size less than 100000,
daddy shows "I need to invest in more companies!".

blob shows "Please, daddy, I need more money to survive!".
daddy shows "Hire some overpaid FAANG workers first!".

create worker with name enzo. enzo salary is 40000. enzo company is "FAANG". enzo role is "product manager".

enzo shows "I have joined blob company! Let's update Linkedin to 'Building' and 'Ex-FAANG'".
enzo company is "blob".

blob shows "I have hired some FAANG workers, daddy!".
daddy shows "Good job, blob! Now you can have more money!".

blob cash is blob cash + 1000000. daddy fund is daddy fund - 1000000.
daddy portfolio_size is daddy portfolio_size + 1.

daddy shows "Now buy some .ai domain and post on ProductHunt! That's what makes great companies".

blob shows blob cash.

while blob cash greater than 0, blob revenue is (500 - 10) * 10, blob expenses is 1000000,
blob cash is blob cash - blob expenses + blob revenue, daddy shows "Blob is going to die, hire more FAANG workers!!!",
blob shows "I can't, daddy, it is not cool to hire post 2021".

blob shows "I have to shut down the company, daddy".

if blob team greater than 0, blob team is 0, blob cash is 0, blob product is "Nothing usefull",
blob revenue is 0, blob expenses is 0, daddy shows "What? I have never invested in blob. He is crazy for posting that on X".
```

## Output

```txt
blob : Let's grow without caring about revenue, burn it all!
blob : Let's grow without caring about revenue, burn it all!
blob : Let's grow without caring about revenue, burn it all!
daddy : I need to invest in more companies!
blob : Please, daddy, I need more money to survive!
daddy : Hire some overpaid FAANG workers first!
enzo : I have joined blob company! Let's update Linkedin to 'Building' and 'Ex-FAANG'
blob : I have hired some FAANG workers, daddy!
daddy : Good job, blob! Now you can have more money!
daddy : Now buy some .ai domain and post on ProductHunt! That's what makes great companies
blob : 1020000
daddy : Blob is going to die, hire more FAANG workers!!!
blob : I can't, daddy, it is not cool to hire post 2021
daddy : Blob is going to die, hire more FAANG workers!!!
blob : I can't, daddy, it is not cool to hire post 2021
blob : I have to shut down the company, daddy
daddy : What? I have never invested in blob. He is crazy for posting that on X
```

## How to Run
To run the code, you need to have Python 3 installed on your machine. Then, you can run the following command on directory root:
```bash
python3 main.py test.zs
```
