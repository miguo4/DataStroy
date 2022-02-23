import random
from .Operator import Operator 

class FindIntersection(Operator):
    def run(self, state):
        # print("find intersection")
        state['type'] = "intersection"
        fields = list(filter(lambda x:x['type'] != 'numerical', self.schema["fields"])) 
        if len(fields) < 1:
            return state
        field = random.choice(fields)
        entity = [
            {
                "field": field["field"],
                "type": field["type"],
                "value": random.choice(field["values"])
            }
        ]
        state["entity"] = entity
        state["facts"][0]["subspace"] = entity
        state["facts"][1]["subspace"] = entity
        return state