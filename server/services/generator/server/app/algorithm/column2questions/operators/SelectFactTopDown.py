import random
from copy import deepcopy
from .Operator import Operator 

fact_template={'fact': 'fact', 'subspace': 'subspace', 'breakdown': 'breakdown', 'measure': 'measure'}
association_template={'fact': '', 'subspace': '', 'breakdown': '', 'measure_1': '','measure_2':''}


class SelectFactTopDown(Operator):

    def run(self, state):
        # fact=self.templatepaired(self.parameter)
        fact=deepcopy(fact_template)
        fact['fact']=self.parameter
        ctg_fields = list(filter(lambda x:x['type'] != 'numerical' and len(x['values']) > 1, self.schema["fields"])) 
        n_fields = list(filter(lambda x:x['type'] == 'numerical', self.schema["fields"])) 
        breakdown_field=random.choice(ctg_fields)
        breakdown=breakdown_field['field']
        measure_1_field=random.choice(n_fields)
        measure_1=measure_1_field['field']
        try:
            measure_2_field=random.choice([x for x in n_fields if x != measure_1_field])
            measure_2=measure_2_field['field']
        except :
            if fact['fact']=='association':
                raise RuntimeError("only one measure in csv")

        subspace_field=random.choice([x for x in ctg_fields if x != breakdown_field])
        subspace=random.choice(subspace_field['values'])

        if fact['fact'] == 'association':
            fact['subspace']=subspace
            fact['breakdown']=breakdown
            fact['measure']=measure_2
            fact['measure_1']=measure_1
        else:
            fact['subspace']=subspace
            fact['breakdown']=breakdown
            fact['measure']=measure_1

        state=fact

        return state

    def templatepaired(self,facttype):
        if facttype == 'association':
            fact=deepcopy(association_template)
            fact['fact']=facttype
        else:
            fact=deepcopy(fact_template)
            fact['fact']=facttype
        return fact
