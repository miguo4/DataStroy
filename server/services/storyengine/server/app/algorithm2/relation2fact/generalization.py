import copy
from .helper import filterfields

def getGeneralizationPossibleFacts(schema, last_fact):
    possibleFacts = []
    facttypes_with_focus = ['outlier', 'proportion', 'extreme', 'difference']
    facttypes_without_focus = ['distribution', 'rank', 'categorization', 'association', 'trend', 'value']
    # Generalization
    # 1. change type remove focus
    if len(last_fact['focus']) > 0:
        for fact_type in facttypes_without_focus:
            new_fact = copy.deepcopy(last_fact)
            new_fact['type'] = fact_type
            if fact_type == 'categorization':
                new_fact['measure'] = []
            if fact_type == 'value':
                new_fact['groupby'] = []
            new_fact['focus'] = []
            possibleFacts.append(new_fact)

    # 2. remove filter
    if len(last_fact['subspace']) > 1:
        for i in (0, 1, 1):
            new_fact = copy.deepcopy(last_fact)
            new_fact['subspace'].pop(i)
            possibleFacts.append(new_fact)
    elif len(last_fact['subspace']) == 1:
        new_fact = copy.deepcopy(last_fact)
        new_fact['subspace'].pop(0)
        possibleFacts.append(new_fact)
    return possibleFacts