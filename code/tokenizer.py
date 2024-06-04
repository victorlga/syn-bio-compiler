import re

class Token:

    def __init__(self, type:str, value:str):
        self.type: str = type
        self.value: str = value

class Tokenizer:

    def __init__(self, source:str):
        self.source: str = source
        self.position: int = 0
        self.next: Token = None
        self.reserved_words_types = {
            'create'            : 'CREATE',
            'with'              : 'WITH',
            'name'              : 'NAME',
            'it'                : 'IT',
            'has'               : 'HAS',
            'of'                : 'OF',
            'is'                : 'IS',
            'shows'             : 'SHOWS',
            'while'             : 'WHILE',
            'if'                : 'IF',
            'hires'             : 'HIRES',
            'layoffs'           : 'LAYOFFS',
            'asks'              : 'ASKS',
            'raise'             : 'RAISE',
            'dies'              : 'DIES',
            'or'                : 'OR',
            'and'               : 'AND',
            'not'               : 'NOT',
            'less'              : 'LESS',
            'greater'           : 'GREATER',
            'than'              : 'THAN',
            'equal'             : 'EQUAL',
            'to'                : 'TO',
            'startup'           : 'STARTUP',
            'venture'           : 'VENTURE',
            'firm'              : 'FIRM',
            'worker'            : 'WORKER',
            'cash'              : 'CASH',
            'revenue'           : 'REVENUE',
            'expenses'          : 'EXPENSES',
            'product'           : 'PRODUCT',
            'team'              : 'TEAM',
            'fund'              : 'FUND',
            'portfolio_size'    : 'PORTFOLIO_SIZE',
            'strategy'          : 'STRATEGY',
            'salary'            : 'SALARY',
            'company'           : 'COMPANY',
            'role'              : 'ROLE',
        }

    def select_next(self):

        value = self._define_value()
        while value in (' ', '\t'):
            self.position += 1
            value = self._define_value()

        if self._end_of_file():
            ctype = 'EOF'
        elif value == '\n':
            ctype = 'NEWLINE'
        elif value == ',':
            ctype = 'COMMA'
        elif value == '.':
            ctype = 'PERIOD'
        elif value == '>':
            ctype = 'BIGGER'
        elif value == '<':
            ctype = 'LOWER'
        elif value == '-':
            ctype = 'MINUS'
        elif value == '+':
            ctype = 'PLUS'
        elif value == '*':
            ctype = 'MULT'
        elif value == '/':
            ctype = 'DIV'
        elif value == '(':
            ctype = 'OPEN_PAR'
        elif value == ')':
            ctype = 'CLOSE_PAR'
        elif value == '=':
            ctype = 'ASSIGN'
        elif value == '"':
            value = ''
            while self.source[self.position+1] != '"':
                self.position += 1
                value += self._define_value(
                    fallback=[SyntaxError, 'Quotation mark is not closed.']
                )
            self.position += 1
            ctype = 'STRING'
        elif value.isdigit():
            while value.isdigit():
                self.position += 1
                value += self._define_value(fallback=' ')
            value = value[:-1]
            ctype = 'INT'
            self.position -= 1
        elif value.isalpha() or value == '_':
            while self._is_valid_variable(value):
                self.position += 1
                value += self._define_value(fallback=' ')
            value = value[:-1]
            self.position -= 1
            is_reserved_word = value in self.reserved_words_types
            ctype = (
                self.reserved_words_types[value]
                if is_reserved_word
                else 'IDENTIFIER'
            )
        else:
            raise ValueError('Not a valid character: ' + value)

        self.position += 1

        self.next = Token(ctype, value)
    
    def _end_of_file(self):
        return self.position >= len(self.source)
    
    def _define_value(self, fallback=''):
        if isinstance(fallback, list) and self._end_of_file():
            raise fallback[0](fallback[1])
        return fallback if self._end_of_file() else self.source[self.position]

    @staticmethod
    def _is_valid_variable(value):
        pattern = r'^[a-zA-Z0-9_]+$'
        return bool(re.match(pattern, repr(value)[1:-1]))
