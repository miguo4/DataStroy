import pandas as pd
from abc import abstractmethod
import sys

sys.path.append("..")
from .IRunable import IRunable
sys.path.pop()


class Operator(IRunable):
    def __init__(self, data, params={}):
        self.data = data
        self.params = params

    def start(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def finish(self):
        pass

    def setProcessor(self):
        pass

    def getProcessor(self):
        pass