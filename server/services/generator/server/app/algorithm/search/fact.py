import re
import json
import traceback
class Fact():
    def __init__(self, type="", measure=[], breakdown=[], subspace=[], focus=[], parameter=[]):
        self.type = type
        self.measure = measure
        self.breakdown = breakdown
        self.subspace = subspace
        self.focus = focus
        self.parameter = parameter

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Fact):
            if self.type != other.type:
                return False
            if self.__compare_two_lists(self.measure, other.measure):
                return False
            if self.__compare_two_lists(self.subspace, other.subspace):
                return False
            if self.__compare_two_lists(self.breakdown, other.breakdown):
                return False
            if self.__compare_two_lists(self.focus, other.focus):
                return False
            return True
        return False

    def __str__(self):
        fact = {
            "type": self.type,
            "measure": self.measure,
            "breakdown": self.breakdown,
            "subspace": self.subspace,
            "focus": self.focus,
            "parameter": self.parameter,

        }
        return json.dumps(fact) 

    def is_fullfilled(self):
        if self.type not in ['categorization', 'extreme', 'trend', 'value', 'association', 'rank', 'distribution', 'outlier', 'difference', 'proportion']:
            return False
        
        if self.type == "association":
            if len(self.measure) < 2:
                return False
        elif self.type == "categorization":
            if len(self.breakdown) < 1:
                return False
        elif self.type == "difference":
            if len(self.measure) < 1 or len(self.breakdown) < 1:
                return False
        elif self.type == "distribution":
            if len(self.measure) < 1 or len(self.breakdown) < 1:
                return False
        elif self.type == "extreme":
            if len(self.measure) < 1 or len(self.breakdown) < 1:
                return False
        elif self.type == "outlier":
            if len(self.measure) < 1 or len(self.breakdown) < 1 or len(self.focus) < 1:
                return False
        elif self.type == "proportion":
            if len(self.measure) < 1 or len(self.breakdown) < 1 or len(self.focus) < 1:
                return False
        elif self.type == "rank":
            if len(self.measure) < 1 or len(self.breakdown) < 1:
                return False
        elif self.type == "trend":
            if len(self.measure) < 1 or len(self.breakdown) < 1:
                return False
        elif self.type == "value":
            if len(self.measure) < 1:
                return False

        return True

    def to_sentence(self):
        template = self.__get_template()
        slots = re.findall("<[^<>]*>", template)
        slots1 = re.findall("<([^<>]*)>", template)
        filled_slots = []
        for slot in slots1:
            try:                
                if slot == 'subspace':
                    filled_slots.append(self.subspace[0]['value'])
                elif slot == 'measure':
                    filled_slots.append(self.measure[0]['field'])
                elif slot == 'breakdown':
                    filled_slots.append(self.breakdown[0]['field'])
                elif slot == 'measure1':
                    filled_slots.append(self.measure[0]['field'])
                elif slot == 'measure2':
                    filled_slots.append(self.measure[1]['field'])
                elif slot == 'focus':
                    filled_slots.append(self.focus[0]['value'])
                elif slot == 'focus1':
                    filled_slots.append(self.focus[0]['value'])
                elif slot == 'focus2':
                    filled_slots.append(self.focus[1]['value'])
                elif slot == 'parameter[1]':
                    filled_slots.append(self.parameter[1])
                elif slot == 'parameter[0]':
                    filled_slots.append(self.parameter[0])
                elif slot == 'parameter':
                    if isinstance(self.parameter, list):
                        filled_slots.append(self.parameter[0])
                    else:
                        filled_slots.append(self.parameter)                
            except Exception as e:
                filled_slots.append('')

        sentence = template

        for i in range(len(slots)):
            sentence = sentence.replace(slots[i], filled_slots[i], 1)

        return sentence

    def __get_template(self):
        templates = {
            "association": "This is the correlation between <measure1> and <measure2> in <subspace>.",
            "categorization": "These are the <breakdown> in <subspace>.",
            "difference": "This is the difference between <focus1> and <focus2> regarding to their <measure> in <subspace>.",
            "distribution": "This is the distribution of the <measure> over different <breakdown> in <subspace>.",
            "extreme": "The <focus> value of the <measure> is an extreme in <subspace>.",
            "outlier": "The <measure> of <focus> is an outlier when compared with that of other <breakdown> when <subspace>.",
            "proportion": "This is the proportion of <focus>'s <measure> in <subspace>.",
            "rank": "This is the <measure> ranking of different <breakdown> in <subspace>.",
            "trend": "This is the <parameter> trend of the <measure> over <breakdown> in <subspace>.",
            "value": "This is the <measure> in <subspace>.",
        }
        return templates[self.type]

    def __compare_two_lists(self, list1, list2):
        """
        Compare two lists and logs the difference.
        :param list1: first list.
        :param list2: second list.
        :return:      if there is difference between both lists.
        """
        diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
        result = len(diff) != 0
        return result

if __name__ == "__main__":
    fact1 = Fact(type="proportion", measure=[{'field': "postgrad student's income", 'aggregate': 'sum', 'type': 'numerical'}], breakdown=[{'field': 'country', 'type': 'geographical'}], subspace=[{'field': 'country', 'type': 'geographical', 'value': 'ireland'}], focus=[{'field': 'country', 'type': 'geographical', 'value': 'costa rica'}])
    fact2 = Fact(type="association", measure=[{'field': "postgrad student's income", 'aggregate': 'sum', 'type': 'numerical'}, {'field': "undergraduate student's income", 'aggregate': 'sum', 'type': 'numerical'}], breakdown=[{'field': 'country', 'type': 'geographical'}], subspace=[{'field': 'country', 'type': 'geographical', 'value': 'switzerland'}], focus=[])
    print(fact1 == fact2)
    print(fact1.to_sentence())
    print(fact2.to_sentence())