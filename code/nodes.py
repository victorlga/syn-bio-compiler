from abc import ABC, abstractmethod
from .table import SymbolTable, params

class Node(ABC):

    def __init__(self, value=None):
        self.value = value
        self.children = []

    @abstractmethod
    def evaluate(self, symbol_table):
        pass

class IdentifierNode(Node):

    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)

class ParameterNode(Node):

    def evaluate(self, symbol_table):
        return self.value, self.children[0].value, self.children[0].evaluate(symbol_table)[0]

class StartupDecNode(Node):

    def evaluate(self, symbol_table):
        symbol_table.set(self.value, "STARTUP", {"CASH":None, "REVENUE":None, "EXPENSES":None, "PRODUCT":None, "TEAM":None})

class WorkerDecNode(Node):

    def evaluate(self, symbol_table):
        symbol_table.set(self.value, "WORKER", {"SALARY":None, "COMPANY":None, "ROLE":None})

class VentureFirmDecNode(Node):

    def evaluate(self, symbol_table):
        symbol_table.set(self.value, "VENTURE", {"FUND":None, "PORTFOLIO_SIZE":None, "STRATEGY":None})

class WhileNode(Node):

    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)

class IfNode(Node):

    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)


class PrintNode(Node):

    def evaluate(self, symbol_table):
        if self.children[1].__class__.__name__ == 'ParameterNode':
            param, key, entity = self.children[1].evaluate(symbol_table)
            if param not in params[entity]:
                raise TypeError(f"Parameter {param} not allowed for {entity}.")
            print(self.children[0].value, ':', symbol_table.get(key)[1][param][0])
            return
        print(self.children[0].value, ':', self.children[1].evaluate(symbol_table)[0])

class AssigmentNode(Node):

    def evaluate(self, symbol_table):

        if self.children[0].__class__.__name__ == 'ParameterNode':
            value = self.children[1].evaluate(symbol_table)
            param, key, entity = self.children[0].evaluate(symbol_table)
            if param not in params[entity]:
                raise TypeError(f"Parameter {param} not allowed for {entity}.")
            param_dict = symbol_table.get(key)[1]
            param_dict[param] = value
            symbol_table.set(key, entity, param_dict)
            return

        value = self.children[1].evaluate(symbol_table)
        key = self.children[0].value
        symbol_table.set(key, value, {})
        self.children[0].evaluate(symbol_table)

class BlockNode(Node):

    def evaluate(self, symbol_table):

        for child in self.children:
            child.evaluate(symbol_table)

class BinOpNode(Node):

    def evaluate(self, symbol_table):

        eval_children_0 = self.children[0].evaluate(symbol_table)
        eval_children_1 = self.children[1].evaluate(symbol_table)

        if self.children[0].__class__.__name__ == 'ParameterNode':
            param, key, entity = eval_children_0
            if param not in params[entity]:
                raise TypeError(f"Parameter {param} not allowed for {entity}.")
            eval_children_0 = symbol_table.get(key)[1][param]
        if self.children[1].__class__.__name__ == 'ParameterNode':
            param, key, entity = eval_children_1
            if param not in params[entity]:
                raise TypeError(f"Parameter {param} not allowed for {entity}.")
            eval_children_1 = symbol_table.get(key)[1][param]

        if self.value == 'PLUS':
            self._check_data_type('INT', eval_children_0, eval_children_1)
            return eval_children_0[0] + eval_children_1[0], 'INT'
        elif self.value == 'MINUS':
            self._check_data_type('INT', eval_children_0, eval_children_1)
            return eval_children_0[0] - eval_children_1[0], 'INT'
        elif self.value == 'MULT':
            self._check_data_type('INT', eval_children_0, eval_children_1)
            return eval_children_0[0] * eval_children_1[0], 'INT'
        elif self.value == 'DIV':
            self._check_data_type('INT', eval_children_0, eval_children_1)
            return eval_children_0[0] // eval_children_1[0], 'INT'
        elif self.value == 'GREATER':
            self._check_data_types_is_equal(eval_children_0, eval_children_1)
            return int(eval_children_0[0] > eval_children_1[0]), 'INT'
        elif self.value == 'LESS':
            self._check_data_types_is_equal(eval_children_0, eval_children_1)
            return int(eval_children_0[0] < eval_children_1[0]), 'INT'
        elif self.value == 'EQUAL':
            self._check_data_types_is_equal(eval_children_0, eval_children_1)
            return int(eval_children_0[0] == eval_children_1[0]), 'INT'
        elif self.value == 'DIFFERENT':
            self._check_data_types_is_equal(eval_children_0, eval_children_1)
            return int(eval_children_0[0] != eval_children_1[0]), 'INT'
        elif self.value == 'AND':
            self._check_data_type('INT', eval_children_0, eval_children_1)
            return int(eval_children_0[0] and eval_children_1[0]), 'INT'
        elif self.value == 'OR':
            self._check_data_type('INT', eval_children_0, eval_children_1)
            return int(eval_children_0[0] or eval_children_1[0]), 'INT'

    def _check_data_type(self, data_type, eval_chil_0, eval_chil_1):
        if eval_chil_0[1] not in data_type or eval_chil_1[1] not in data_type:
                raise TypeError(f'"{self.value}" operator is only allowed with ' + data_type + ' data.')
        
    def _check_data_types_is_equal(self, eval_chil_0, eval_chil_1):
        if eval_chil_0[1] != eval_chil_1[1]:
            raise TypeError(f'"{self.value}" operator can\'t be used between data with different types.')

class UnOpNode(Node):

    def evaluate(self, symbol_table):
        if self.value == '+':
            return self.children[0].evaluate(symbol_table)[0], 'INT'
        elif self.value == '-':
            return -self.children[0].evaluate(symbol_table)[0], 'INT'
        elif self.value == 'not':
            return not self.children[0].evaluate(symbol_table)[0], 'INT'

class IntValNode(Node):

    def evaluate(self, symbol_table):
        return int(self.value), 'INT'

class StringNode(Node):

    def evaluate(self, symbol_table):
        return str(self.value), 'STRING'

class NoOpNode(Node):

    def evaluate(self, symbol_table):
        pass