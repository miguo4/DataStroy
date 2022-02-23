from .operators import *
from .SlotsFilling import SlotsFilling
import os
import json
import csv
import random

class SimpleQuestionGenerator:
    def __init__(self):
        self.__schema = {}
        with open('templates/simple.json') as f:
            self.__templates = json.load(f)

    def load(self, schema):
        # load data schema
        self.__schema = schema

    def generate(self): #input templates and schema ; return corpus 
        simples = self.__templates
        sq_template_json=[]
        sf = SlotsFilling()
        sf.load(self.__schema)
        for simple in simples:
            try:
                question_json=sf.slotsfilling_from_template(simple)
                sq_template_json.append(question_json)
            except:
                pass

        return sq_template_json


    def generate_from_fact(self,fact): #input fact, templates and schema ; return corpus 
        simples = self.__templates
        sf = SlotsFilling()
        sf.load(self.__schema)
        sq_fact_json=sf.slotsfilling_from_fact(simples,fact)
        if len(sq_fact_json) == 0:
            return ""
        # random pick
        simple_question = random.choice(sq_fact_json)
        return simple_question["question"]
    
                
