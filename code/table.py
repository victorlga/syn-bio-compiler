class SymbolTable:

    def __init__(self):
        self.table = {}

    def get(self, key):
        return self.table[key]

    def set(self, key, value, param):
        self.table[key] = [value, param]

venture_params = (
    "FUND", "PORTFOLIO_SIZE", "STRATEGY",
)

startup_params = (
    "CASH", "REVENUE", "EXPENSES", "PRODUCT", "TEAM",
)

worker_params = (
    "SALARY", "COMPANY", "ROLE",
)

params = {
    "VENTURE"   : venture_params,
    "STARTUP"   : startup_params,
    "WORKER"    : worker_params,
}