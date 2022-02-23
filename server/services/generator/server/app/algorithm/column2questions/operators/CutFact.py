import random
from .Operator import Operator 
import itertools
from copy import deepcopy

class CutFact(Operator):

    
    def run(self, state):
        cut_parameter=deepcopy(self.parameter)
        cutfact=deepcopy(state)
        # print(selectfact)
        cutted_fact = [k for k, v in cut_parameter.items() if v =='*']
        for i in cutted_fact:
            cutfact[i]='*'
        return cutfact