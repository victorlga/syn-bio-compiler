from .tokenizer import Tokenizer
from .preprocessing import filter
from .nodes import (
    BinOpNode, IntValNode, UnOpNode, PrintNode, AssigmentNode, BlockNode,
    IdentifierNode, NoOpNode, IfNode, WhileNode, StringNode, WorkerDecNode,
    StartupDecNode, VentureFirmDecNode, DiesNode, LayoffNode, HireNode,
    AskNode, ParameterNode
)

class Parser:

    def __init__(self):
        self.tokenizer = None

    def run(self, raw_source):
        source = filter(raw_source)
        self.tokenizer = Tokenizer(source)
        self.tokenizer.select_next()
        ast_root = self._parse_block()
        return ast_root

    def _select_and_check_unexpected_token(self, select, *expected_tokens):
        if select:
            self.tokenizer.select_next()
        if self.tokenizer.next.type not in expected_tokens:
            raise ValueError(f'Expected one of {expected_tokens} token types, got: {self.tokenizer.next.type}')

    def _parse_block(self):

        block_node = BlockNode()

        while self.tokenizer.next.type != 'EOF':
            statement = self._parse_statement()
            block_node.children.append(statement)
            self._select_and_check_unexpected_token(False, 'PERIOD', 'NEWLINE')
            self.tokenizer.select_next()

        return block_node

    def _parse_statement(self):

        token = self.tokenizer.next

        if token.type == 'CREATE':
            self.tokenizer.select_next()
            match self.tokenizer.next.type:
                case 'WORKER':
                    self._select_and_check_unexpected_token(True, 'WITH')
                    self._select_and_check_unexpected_token(True, 'NAME')
                    self._select_and_check_unexpected_token(True, 'IDENTIFIER')
                    entity_dec_node = WorkerDecNode(self.tokenizer.next.value)
                case 'STARTUP':
                    self._select_and_check_unexpected_token(True, 'WITH')
                    self._select_and_check_unexpected_token(True, 'NAME')
                    self._select_and_check_unexpected_token(True, 'IDENTIFIER')
                    entity_dec_node = StartupDecNode(self.tokenizer.next.value)
                case 'VENTURE':
                    self._select_and_check_unexpected_token(True, 'FIRM')
                    self._select_and_check_unexpected_token(True, 'WITH')
                    self._select_and_check_unexpected_token(True, 'NAME')
                    self._select_and_check_unexpected_token(True, 'IDENTIFIER')
                    entity_dec_node = VentureFirmDecNode(self.tokenizer.next.value)
                case _:
                    raise ValueError(f'Unexpected token: {self.tokenizer.next.type}')
            self.tokenizer.select_next()
            return entity_dec_node

        elif token.type == 'IDENTIFIER':
            identifier_node = IdentifierNode(token.value)
            self.tokenizer.select_next()

            if self.tokenizer.next.type == 'SHOWS':
                print_node = PrintNode()
                print_node.children.append(identifier_node)

                self.tokenizer.select_next()
                bool_expression = self._parse_bool_expression()
                print_node.children.append(bool_expression)

                return print_node

            elif self.tokenizer.next.type == 'DIES':
                dies_node = DiesNode()
                dies_node.children.append(identifier_node)
                self.tokenizer.select_next()
                return dies_node

            elif self.tokenizer.next.type == 'LAYOFFS':
                layoff_node = LayoffNode()
                layoff_node.children.append(identifier_node)
                self.tokenizer.select_next()
                return layoff_node

            elif self.tokenizer.next.type == 'HIRES':
                hire_node = HireNode()
                hire_node.children.append(identifier_node)
                self._select_and_check_unexpected_token(True, 'IDENTIFIER')
                identifier_node = IdentifierNode(self.tokenizer.next.value)
                hire_node.children.append(identifier_node)
                self.tokenizer.select_next()
                return hire_node

            elif self.tokenizer.next.type == 'ASKS':
                ask_node = AskNode()
                ask_node.children.append(identifier_node)
                self._select_and_check_unexpected_token(True, 'IDENTIFIER')
                identifier_node = IdentifierNode(self.tokenizer.next.value)
                ask_node.children.append(identifier_node)
                self._select_and_check_unexpected_token(True, 'TO')
                self._select_and_check_unexpected_token(True, 'RAISE')
                self.tokenizer.select_next()
                bool_expression = self._parse_bool_expression()
                ask_node.children.append(bool_expression)
                return ask_node

            elif self._is_parameter(self.tokenizer.next.type):
                parameter_node = ParameterNode(self.tokenizer.next.value)
                self._select_and_check_unexpected_token(True, 'IS')
                parameter_node.children.append(identifier_node)
                assigment_node = AssigmentNode()
                assigment_node.children.append(parameter_node)
                self.tokenizer.select_next()
                bool_expression = self._parse_bool_expression()
                assigment_node.children.append(bool_expression)
                return assigment_node

        elif token.type == 'WHILE':
            while_node = WhileNode()

            self.tokenizer.select_next()
            bool_expression = self._parse_bool_expression()
            while_node.children.append(bool_expression)

            self._select_and_check_unexpected_token(False, 'COMMA')
            block_node = BlockNode()

            self.tokenizer.select_next()
            while self.tokenizer.next.type != 'PERIOD':
                if self.tokenizer.next.type == 'COMMA':
                    self.tokenizer.select_next()
                if self.tokenizer.next.type == 'NEWLINE':
                    self.tokenizer.select_next()
                statement = self._parse_statement()
                block_node.children.append(statement)

            while_node.children.append(block_node)
            return while_node
        elif token.type == 'IF':
            if_node = IfNode()

            self.tokenizer.select_next()
            bool_expression = self._parse_bool_expression()
            if_node.children.append(bool_expression)

            self._select_and_check_unexpected_token(False, 'COMMA')

            block_node = BlockNode()

            self.tokenizer.select_next()
            while self.tokenizer.next.type != 'PERIOD':
                if self.tokenizer.next.type == 'COMMA':
                    self.tokenizer.select_next()
                if self.tokenizer.next.type == 'NEWLINE':
                    self.tokenizer.select_next()
                statement = self._parse_statement()
                block_node.children.append(statement)

            if_node.children.append(block_node)
            return if_node

        self._select_and_check_unexpected_token(False, 'NEWLINE')
        return NoOpNode()

    def _binop_parse_template(self, parsing_func, binop_types):
        node = parsing_func()
        result = node

        token = self.tokenizer.next

        while token.type in binop_types:
            if token.type in {'LESS', 'GREATER', 'EQUAL'}:
                self.tokenizer.select_next()

            binop = BinOpNode(token.type)
            binop.children.append(result)

            self.tokenizer.select_next()
            node = parsing_func()
            binop.children.append(node)

            token = self.tokenizer.next
            result = binop

        return result

    def _parse_bool_expression(self):
        return self._binop_parse_template(self._parse_bool_term, {'OR'})

    def _parse_bool_term(self):
        return self._binop_parse_template(self._parse_relational_expression, {'AND'})

    def _parse_relational_expression(self):
        return self._binop_parse_template(self._parse_expression, {'LESS', 'GREATER', 'EQUAL'})

    def _parse_expression(self):
        return self._binop_parse_template(self._parse_term, {'PLUS', 'MINUS'})

    def _parse_term(self):
        return self._binop_parse_template(self._parse_factor, {'MULT', 'DIV'})

    def _parse_factor(self):

        token = self.tokenizer.next

        if token.type == 'IDENTIFIER':
            identifier_node = IdentifierNode(token.value)
            self.tokenizer.select_next()
            if self._is_parameter(self.tokenizer.next.type):
                parameter_node = ParameterNode(self.tokenizer.next.value)
                parameter_node.children.append(identifier_node)
                self.tokenizer.select_next()
                return parameter_node
            return identifier_node
        elif token.type == 'STRING':
            self.tokenizer.select_next()
            return StringNode(token.value)
        elif token.type == 'INT':
            self.tokenizer.select_next()
            return IntValNode(token.value)
        elif token.type in ('PLUS', 'MINUS', 'NOT'):
            self.tokenizer.select_next()
            factor = self._parse_factor()
            unop = UnOpNode(token.value)
            unop.children.append(factor)
            return unop
        elif token.type == 'OPEN_PAR':
            self.tokenizer.select_next()
            expression = self._parse_bool_expression()
            self._select_and_check_unexpected_token(False, 'CLOSE_PAR')
            self.tokenizer.select_next()
            return expression

    def _is_parameter(self, token_type):
        return token_type in {
            "CASH" , "REVENUE" , "EXPENSES" , "PRODUCT",
            "TEAM", "FUND", "PORTFOLIO_SIZE", "STRATEGY",
            "SALARY", "COMPANY", "ROLE"
        }
