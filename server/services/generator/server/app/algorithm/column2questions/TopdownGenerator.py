import os
import json
import csv
from copy import deepcopy
from .operators import *
from .CQGenerator import ComplexQuestionGenerator
from .SQGenerator import SimpleQuestionGenerator
import itertools
import re
import random

class TopdownQuestionGenerator(ComplexQuestionGenerator):
    def __init__(self):
        super().__init__()
        with open('./templates/topdown.json') as json_file:
            self.templates = json.load(json_file)
            self.template_fact = list(map(lambda x: {
                                      "fact": x["fact"], "subspace": x["subspace"], "breakdown": x["breakdown"], "measure": x["measure"]}, self.templates))
            self.template_question = list(
                map(lambda x: x["template"], self.templates))

    def generate(self):
        schema = self.schema
        template_fact = self.template_fact
        template_question = self.template_question
        total_cut_parameters = []
        selectFactOps = []
        cutFactOps = []
        total_cut_facts = []

        for i in range(2):
            cut_facts=[]
            question_json = []
            for facttype in ['association' , 'value', 'difference', 'proportion', 'trend', 'categorization', 'distribution', 'rank', 'outlier', 'extreme']:
                selectfact = SelectFactTopDown(schema, parameter=facttype)
                selectFactOps.append(selectfact)

            fact = {
                'fact': 'fact',
                'subspace': 'subspace',
                'breakdown': 'breakdown',
                'measure': 'measure'
            }

            for num in range(len(fact)):
                cut_lists = self.cut_parameter_generation(
                    num, fact, total_cut_parameters)
                for cut_list in cut_lists:
                    cutfact = CutFact(schema, parameter=cut_list)
                    cutFactOps.append(cutfact)

            for selectOpt in selectFactOps:
                for cutOpt in cutFactOps:
                    try:
                        state = {}
                        self.add_operator(selectOpt)
                        self.add_operator(cutOpt)
                        cutfact = self.run_operators(state)
                        if cutfact not in total_cut_facts:
                            cut_facts.append(cutfact)
                            total_cut_facts.append(cutfact)
                    except Exception as e:
                        print(e)
                        break

            for cutfact in cut_facts:
                try:
                    question_template = self.question_template_paired(
                        template_fact, cutfact, template_question)
                    for ques_temp in question_template:
                        question = self.question_write(ques_temp, cutfact)
                        question=question.lower()
                        qsjson = {}
                        cutfact['focus'] = '*'
                        qsjson['fact'] = cutfact
                        qsjson['question'] = question
                        question_json.append(qsjson)
                except Exception as e:
                    print(e)

        random.shuffle(question_json)   
        return question_json



    def question_write(self, question_template, cutfact_1):
        slots = re.findall('<[^<>]*>', question_template)
        question = deepcopy(question_template)
        if len(slots) == 0:
            return question_template
        else:
            for slot in slots:
                question = question.replace(
                    slot, cutfact_1[re.sub(r"[<>]", "", slot)])
            return question

    def question_template_paired(self, template_fact, cutfact_1, template_question):
        question_template=[]
        paired_template = [x for x in template_fact if [k for k, v in x.items(
        ) if v == '*'] == [k for k, v in cutfact_1.items() if v == '*'] and x['fact'] == cutfact_1['fact']]
        if len(paired_template) == 0:
            raise RuntimeError(
                '%s does not match with any template' % (cutfact_1))
        elif len(paired_template) == 2:
            for fact, question in zip(template_fact, template_question):
                if fact == paired_template[0]:
                    question_template.append(question)

                if fact == paired_template[1]:
                    question_template.append(question)
        else:
            for fact, question in zip(template_fact, template_question):
                if fact == paired_template[0]:
                    question_template.append(question)
        
        return question_template

    def cut_parameter_generation(self, fact_len, fact, total_cut_parameters):
        cut_list = []
        if fact_len == 0:
            cut_parameter = deepcopy(fact)
            for i in list(cut_parameter.keys()):
                cut_parameter[i] = '*'
            total_cut_parameters.append(cut_parameter)
            cut_list.append(cut_parameter)
        else:
            ite = list(itertools.combinations(fact, fact_len))
            for i in ite:
                picke_element = list(i)
                cut_parameter = deepcopy(fact)
                for element in [x for x in list(fact.keys()) if x not in picke_element]:
                    cut_parameter[element] = '*'
                    if cut_parameter not in total_cut_parameters:
                        total_cut_parameters.append(cut_parameter)
                        cut_list.append(cut_parameter)

        return cut_list
