import random
from .Operator import Operator 

class FindComp(Operator):
    def run(self, state):
        # print("find comparative subspaces")
        state['type'] = "comparison"
        entity = [
            {
                "field": "test",
                "value": "subspace1"
            },
            {
                "field": "test",
                "value": "subspace2"
            }
        ]
        fields = list(filter(lambda x:x['type'] != 'numerical' and len(x['values']) > 1, self.schema["fields"])) 
        if len(fields) < 1:
            return state
        field = random.choice(fields)
        values = random.sample(field["values"], 2)
        entity = [
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
        state["entity"] = entity
        state["facts"][0]["subspace"] = [entity[0]]
        state["facts"][1]["subspace"] = [entity[1]]
        return state