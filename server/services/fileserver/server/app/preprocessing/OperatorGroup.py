import pandas as pd
from abc import abstractmethod
from .IRunable import IRunable

class OperatorGroup(IRunable):
    def __init__(self, data, parallel = False, params={}):
        self.data = data
        self.operators = []
        self.parallel = parallel
        self.params = params

    def __getitem__(self,index):
        return self.operators[index]

    def __setitem__(self, index, operator):
        self.operators[index] = operator

    def __len__(self):
        return len(self.operators)

    def add(self, operator):
        self.operators.append(operator)

    def remove(self):
        if len(self.operators > 0):
            self.operators.pop()

    def clear(self):
        self.operators = []

    def optimize(self):
        #optimize the order of operators in group
        return

    def run(self):
        if self.parallel:
            #create multithread to run operators
            pass
        else:
            self.optimize()
            for op in self.operators:
                # op.getProcessor()
                op.start()
                op.run()
                op.finish()
                self.data.merge(op.data)

        return self.data
        

