import pandas as pd
from .OperatorGroup import OperatorGroup

class Processor:
    def __init__(self, data):
        #initiate an empty pipeline of operators
        self.data=data
        self.operators = OperatorGroup(data = data)
        return

    def getData(self):
        return self.data 

    def __getitem__(self, index):
        return self.operators[index]

    def __setitem__(self, index, operator):
        self.operators[index] = operator

    def __len__(self):
        return len(self.operators)

    def add(self, operator):
        self.operators.add(operator)

    def remove(self):
        self.operators.remove()

    def clear(self):
        self.operators.clear()

    def optimize(self):
        #optimize the order of operators
        return

    def run(self):
        self.optimize()
        #iterate the pipeline to excute the operators sequentially
        return self.operators.run()
