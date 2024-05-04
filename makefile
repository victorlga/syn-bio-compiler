all: parser

parser: src/parser.y src/lexer.l
	bison -d -Wcounterexamples src/parser.y -o src/parser.tab.c
	flex -o src/lex.yy.c src/lexer.l
	gcc -o parser src/parser.tab.c src/lex.yy.c -lfl

clean:
	rm -f src/parser.tab.c src/parser.tab.h src/lex.yy.c parser