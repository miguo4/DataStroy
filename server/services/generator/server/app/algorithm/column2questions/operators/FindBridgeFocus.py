import random
from .Operator import Operator 

class FindBridgeFocus(Operator):

    def run(self, state):
        # print("find bridge focus")
        state['type'] = "bridge_focus"
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
        state["facts"][0]["breakdown"] = [
            {
                "field": field["field"],
                "type": field["type"]
            }
        ]
        state["entity"] = entity
        state["facts"][0]["focus"] = entity
        state["facts"][1]["subspace"] = entity
        return state