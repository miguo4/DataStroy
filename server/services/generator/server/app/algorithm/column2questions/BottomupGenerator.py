import os
import json
import csv
from copy import deepcopy
from .operators import *
from .CQGenerator import ComplexQuestionGenerator
from .SQGenerator import SimpleQuestionGenerator
import random
default_state = {
    "type": "",
    "entity": [],
    "facts": [
        {
            "type": "",
            "subspace": [],
            "measure": [],
            "breakdown": [],
            "focus": []
        },
        {
            "type": "",
            "subspace": [],
            "measure": [],
            "breakdown": [],
            "focus": []
        }
    ]
}

class BottomupQuestionGenerator(ComplexQuestionGenerator):
    def __init__(self):
        super().__init__()
        with open('./templates/bottomup.json') as json_file:
            self.templates = json.load(json_file)
            self.rule = list(map(lambda x:{"type":x["type"], "fact1":x["fact1"], "fact2":x["fact2"], "logic":x["logic"]}, self.templates))

    def get_template(self, question_type, fact1_type, fact2_type):
        templates = list(filter(lambda x:x['type'] == question_type and x['fact1'] == fact1_type and x['fact2'] == fact2_type and x['logic'] == True, self.templates))
        if len(templates) > 0:
            return templates[0]['template']
        else:
            return ""

    def write_question(self, qcspec):
        cq_type = qcspec['type']
        fact1 = qcspec['facts'][0]
        fact1_type = fact1['type']
        fact2 = qcspec['facts'][1]
        fact2_type = fact2['type']
        question = self.get_template(cq_type, fact1_type, fact2_type)

        if cq_type == "comparison":
            question = question.replace("<comp_1>", qcspec["entity"][0]["value"])
            question = question.replace("<comp_2>", qcspec["entity"][1]["value"])
        elif cq_type == "intersection":
            question = question.replace("<intersection>", qcspec["entity"][0]["field"])
        else:
            question = question.replace("<bridge>", qcspec["entity"][0]["field"])
        
        try:
            question = question.replace("<measure_1>", qcspec["facts"][0]["measure"][0]["field"])
        except:
            pass
        
        if "<measure_1_1>" in question and "<measure_1_2>" in question:
            try:
                question = question.replace("<measure_1_1>", qcspec["facts"][0]["measure"][0]["field"])
                question = question.replace("<measure_1_2>", qcspec["facts"][0]["measure"][1]["field"])
            except:
                question=''

        try:
            question = question.replace("<measure_2>", qcspec["facts"][1]["measure"][0]["field"])
        except:
            pass
        
        if "<measure_2_1>" in question and "<measure_2_2>" in question:
            try:
                question = question.replace("<measure_2_1>", qcspec["facts"][0]["measure"][0]["field"])
                question = question.replace("<measure_2_2>", qcspec["facts"][0]["measure"][1]["field"])
            except:
                question=''

        
        try:
            question = question.replace("<breakdown_1>", qcspec["facts"][0]["breakdown"][0]["field"])
        except:
            pass
        try:
            question = question.replace("<breakdown_2>", qcspec["facts"][1]["breakdown"][0]["field"])
        except:
            pass
        
        try:
            question = question.replace("<focus_1>", qcspec["facts"][0]["focus"][0]["value"])
        except:
            pass
        try:
            question = question.replace("<focus_1_1>", qcspec["facts"][0]["focus"][0]["value"])
        except:
            pass
        try:
            question = question.replace("<focus_1_2>", qcspec["facts"][0]["focus"][1]["value"])
        except:
            pass
        try:
            question = question.replace("<focus_2>", qcspec["facts"][1]["focus"][0]["value"])
        except:
            pass
        try:
            question = question.replace("<focus_2_1>", qcspec["facts"][1]["focus"][0]["value"])
        except:
            pass
        try:
            question = question.replace("<focus_2_2>", qcspec["facts"][1]["focus"][1]["value"])
        except:
            pass

        return question
        
    def generate(self):
        schema = self.schema
        rule = self.rule
        findbridgefocus = FindBridgeFocus(schema)
        findbridgesubspace = FindBridgeSubspace(schema)
        findintersection = FindIntersection(schema)
        findcomp = FindComp(schema)
        selectfact = SelectFact(schema, rule)

        question_json = []

        for _ in range(100):
            self.add_operator(findbridgefocus)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            if question != '':
                question=question.lower()
                qsjson["question"] = question
                question_json.append(qsjson)

        for _ in range(100):
            self.add_operator(findbridgesubspace)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            if question != '':
                question=question.lower()
                qsjson["question"] = question
                question_json.append(qsjson)
        
        for _ in range(100):
            self.add_operator(findcomp)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            if question != '':
                question=question.lower()
                qsjson["question"] = question
                question_json.append(qsjson)

        for _ in range(100):
            self.add_operator(findintersection)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            if question != '':
                question=question.lower()
                qsjson["question"] = question
                question_json.append(qsjson)
        random.shuffle(question_json)   
        return question_json


    def generate_paired(self):
        schema = self.schema
        rule = self.rule
        sg = SimpleQuestionGenerator()
        sg.load(schema)
        findbridgefocus = FindBridgeFocus(schema)
        findbridgesubspace = FindBridgeSubspace(schema)
        findintersection = FindIntersection(schema)
        findcomp = FindComp(schema)
        selectfact = SelectFact(schema, rule)

        question_json = []

        for _ in range(100):
            self.add_operator(findbridgefocus)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            qsjson["question"] = question
            qsjson["sub-question-1"] = sg.generate_from_fact(qsjson['facts'][0])
            qsjson["sub-question-2"] = sg.generate_from_fact(qsjson['facts'][1])
            question_json.append(qsjson)

        for _ in range(100):
            self.add_operator(findbridgesubspace)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            qsjson["question"] = question
            qsjson["sub-question-1"] = sg.generate_from_fact(qsjson['facts'][0])
            qsjson["sub-question-2"] = sg.generate_from_fact(qsjson['facts'][1])
            question_json.append(qsjson)
        
        for _ in range(100):
            self.add_operator(findcomp)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            qsjson["question"] = question
            qsjson["sub-question-1"] = sg.generate_from_fact(qsjson['facts'][0])
            qsjson["sub-question-2"] = sg.generate_from_fact(qsjson['facts'][1])
            question_json.append(qsjson)

        for _ in range(100):
            self.add_operator(findintersection)
            self.add_operator(selectfact)
            state = deepcopy(default_state)
            qsjson = self.run_operators(state)
            question = self.write_question(qsjson)
            qsjson["question"] = question
            qsjson["sub-question-1"] = sg.generate_from_fact(qsjson['facts'][0])
            qsjson["sub-question-2"] = sg.generate_from_fact(qsjson['facts'][1])
            question_json.append(qsjson)

        return question_json


if __name__ == "__main__":
    cg = BottomupQuestionGenerator()
    with open('./schema/CarSales.json') as schema_json:
        schema = json.load(schema_json)
        cg.load(schema)
        cg.generate()