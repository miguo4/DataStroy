import pandas as pd
from abc import ABCMeta, abstractmethod

class IRunable(metaclass = ABCMeta):
    @abstractmethod
    def run(self, data):
        pass
