class Operator:
    def __init__(self, schema, rule=[], parameter = {}):
        self.schema = schema
        self.rule = rule
        self.parameter = parameter

    def run(self, state):
        return state
