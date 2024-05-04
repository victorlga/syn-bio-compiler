parser: src/lexer.l src/parser.y
	bison -d src/parser.y
	lex src/lexer.l
	gcc -o $@ parser.tab.c lex.yy.c -lfl

clean:
	rm -f parser
	rm -f lex.yy.c
	rm -f parser.tab.c
	rm -f parser.tab.h
