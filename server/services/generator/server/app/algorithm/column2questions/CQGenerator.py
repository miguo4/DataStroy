import os
import json
import csv
from .operators import *

class ComplexQuestionGenerator:
    def __init__(self):
        self.schema = {}
        self.operators = []
        self.templates = []
        self.rule = []

    def load(self, schema):
        # load data schema
        self.schema = schema

    def add_operator(self, operator):
        self.operators.append(operator)

    def run_operators(self, state):
        # pop operators
        while self.operators:
            operator = self.operators.pop(0)
            state = operator.run(state)

        return state

    def generate(self):
        return []
