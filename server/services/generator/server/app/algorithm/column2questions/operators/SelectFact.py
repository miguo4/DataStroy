import random
from copy import deepcopy
from .Operator import Operator 

fact_with_2_measure = ["association"]
fact_with_1_measure = ["extreme", "difference", "distribution", "proportion", "rank", "outlier", "trend", "value"]
fact_without_breakdown = ["value"]
fact_with_2_focus = ["difference"]
fact_with_1_focus = ["extreme", "rank", "outlier", "proportion"]

class SelectFact(Operator):

    def run(self, state):
        # print("select facts")
        ctg_fields = list(filter(lambda x:x['type'] != 'numerical' and len(x['values']) > 1, self.schema["fields"])) 
        t_fields = list(filter(lambda x:x['type'] == 'temporal' and len(x['values']) > 1, self.schema["fields"])) 
        n_fields = list(filter(lambda x:x['type'] == 'numerical', self.schema["fields"])) 

        selected_rules = list(filter(lambda x:x['type'] == state["type"] and x['logic'] == True , self.rule)) 
        selected_rule = random.choice(selected_rules)

        fact1 = state["facts"][0]
        fact1["type"] = selected_rule["fact1"]
        if fact1["measure"] == []:
            if fact1["type"] in fact_with_2_measure and len(n_fields) > 1:
                selected_measures = random.sample(n_fields, 2)
                selected_measures = list(map(lambda x:{"field": x["field"], "aggregate": "sum", "type": "numerical"}, selected_measures))
                fact1["measure"] = selected_measures
            elif fact1["type"] in fact_with_1_measure and len(n_fields) > 0:
                selected_measures = random.sample(n_fields, 1)
                selected_measures = list(map(lambda x:{"field": x["field"], "aggregate": "sum", "type": "numerical"}, selected_measures))
                fact1["measure"] = selected_measures
        if fact1["breakdown"] == []:
            if fact1["type"] == "trend":
                if len(t_fields) > 0:
                    selected_breakdown = random.sample(t_fields, 1)
                    selected_breakdown = list(map(lambda x:{"field": x["field"], "type": x["type"]}, selected_breakdown))
                    fact1["breakdown"] = selected_breakdown
            elif fact1["type"] not in fact_without_breakdown:
                selected_breakdown = random.sample(ctg_fields, 1)
                selected_breakdown = list(map(lambda x:{"field": x["field"], "type": x["type"]}, selected_breakdown))
                fact1["breakdown"] = selected_breakdown
        if fact1["focus"] == []:
            if fact1["type"] in fact_with_2_focus:
                field = list(filter(lambda x:x['field'] == fact1["breakdown"][0]['field'], ctg_fields))[0]
                values = field["values"]
                values = random.sample(values, 2)
                fact1["focus"] = [
                    {
                        "field": field["field"],
                        "type": field["type"],
                        "value": values[0]
                    },
                    {
                        "field": field["field"],
                        "type": field["type"],
                        "value": values[1]
                    }
                ]
            elif fact1["type"] in fact_with_1_focus:
                field = list(filter(lambda x:x['field'] == fact1["breakdown"][0]['field'], ctg_fields))[0]
                values = field["values"]
                fact1["focus"] = [
                    {
                        "field": field["field"],
                        "type": field["type"],
                        "value": random.choice(values)
                    }
                ]
        

        fact2 = state["facts"][1]
        fact2["type"] = selected_rule["fact2"]
        if fact2["measure"] == []:
            if fact2["type"] in fact_with_2_measure and len(n_fields) > 1:
                selected_measures = random.sample(n_fields, 2)
                selected_measures = list(map(lambda x:{"field": x["field"], "aggregate": "sum", "type": "numerical"}, selected_measures))
                fact2["measure"] = selected_measures
            elif fact2["type"] in fact_with_1_measure and len(n_fields) > 0:
                selected_measures = random.sample(n_fields, 1)
                selected_measures = list(map(lambda x:{"field": x["field"], "aggregate": "sum", "type": "numerical"}, selected_measures))
                fact2["measure"] = selected_measures
        if fact2["breakdown"] == []:
            if fact2["type"] == "trend":
                if len(t_fields) > 0:
                    selected_breakdown = random.sample(t_fields, 1)
                    selected_breakdown = list(map(lambda x:{"field": x["field"], "type": x["type"]}, selected_breakdown))
                    fact2["breakdown"] = selected_breakdown
            elif fact2["type"] not in fact_without_breakdown:
                selected_breakdown = random.sample(ctg_fields, 1)
                selected_breakdown = list(map(lambda x:{"field": x["field"], "type": x["type"]}, selected_breakdown))
                fact2["breakdown"] = selected_breakdown
        if fact2["focus"] == []:
            if fact2["type"] in fact_with_2_focus:
                field = list(filter(lambda x:x['field'] == fact2["breakdown"][0]['field'], ctg_fields))[0]
                values = field["values"]
                values = random.sample(values, 2)
                fact2["focus"] = [
                    {
                        "field": field["field"],
                        "type": field["type"],
                        "value": values[0]
                    },
                    {
                        "field": field["field"],
                        "type": field["type"],
                        "value": values[1]
                    }
                ]
            elif fact2["type"] in fact_with_1_focus:
                field = list(filter(lambda x:x['field'] == fact2["breakdown"][0]['field'], ctg_fields))[0]
                values = field["values"]
                fact2["focus"] = [
                    {
                        "field": field["field"],
                        "type": field["type"],
                        "value": random.choice(values)
                    }
                ]

        state["facts"][0] = fact1
        state["facts"][1] = fact2

        return state