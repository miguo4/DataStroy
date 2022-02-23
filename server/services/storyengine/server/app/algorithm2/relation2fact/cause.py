import copy
from .helper import filterfields

def getCauseEffectPossibleFacts(df, schema, last_fact):
    n_fields = filterfields(schema, 'numerical')
    possibleFacts = []
    # Cause 
    # 1. change measure # TODO: use causality discover technique
    if len(last_fact['measure']) != 0 and len(n_fields) > 1:
        last_measure = last_fact['measure'][0]['field']
        for field in n_fields:
            if last_measure == field['field']:
                continue
            new_fact = copy.deepcopy(last_fact)
            new_fact['measure'][0]['field'] = field['field']
            possibleFacts.append(new_fact)
    return possibleFacts