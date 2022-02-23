import copy
from ..fact import fact_scoring
from .helper import filterfields

def getContrastPossibleFacts(df, schema, method, last_fact):
    n_fields = filterfields(schema, 'numerical')
    c_fields = filterfields(schema, 'categorical')
    t_fields = filterfields(schema, 'temporal')
    g_fields = filterfields(schema, 'geographical')
    ctg_fields = c_fields + t_fields + g_fields
    possibleFacts = []
    # Contrast 
    # filter unsupported 
    supported_facttypes = ['rank', 'proportion', 'trend']
    if last_fact['type'] not in supported_facttypes:
        return possibleFacts
    # get parameter
    _, last_parameter, _, _, _ = fact_scoring(last_fact, df, schema, method)

    # 1. change measure  
    if len(last_fact['measure']) != 0 and len(n_fields) > 1:
        last_measure = last_fact['measure'][0]['field']
        for field in n_fields:
            if last_measure == field['field']:
                continue
            new_fact = copy.deepcopy(last_fact)
            new_fact['measure'][0]['field'] = field['field']
            if check_contrast(new_fact, df, schema, last_parameter, method):
                possibleFacts.append(new_fact)            
    # 2. add filter (not more than 2)
    if len(last_fact['subspace']) == 0:
        for field in ctg_fields:
            if len(last_fact['groupby']) > 0 and last_fact['groupby'][0] == field['field']:
                continue
            if 'values' in field:
                for value in field['values']:
                    new_fact = copy.deepcopy(last_fact)
                    new_fact['subspace'].append({})
                    new_fact['subspace'][0]['field'] = field['field']
                    new_fact['subspace'][0]['value'] = value
                    if check_contrast(new_fact, df, schema, last_parameter, method):
                        possibleFacts.append(new_fact)
    elif len(last_fact['subspace']) == 1:
        for field in ctg_fields:
            if last_fact['subspace'][0]['field'] == field['field']:
                continue
            if len(last_fact['groupby']) > 0 and last_fact['groupby'][0] == field['field']:
                continue
            if 'values' in field:
                for value in field['values']:
                    new_fact = copy.deepcopy(last_fact)
                    new_fact['subspace'].append({})
                    new_fact['subspace'][1]['field'] = field['field']
                    new_fact['subspace'][1]['value'] = value
                    if check_contrast(new_fact, df, schema, last_parameter, method):
                        possibleFacts.append(new_fact)
    # 3. remove filter
    if len(last_fact['subspace']) > 1:
        for i in (0, 1, 1):
            new_fact = copy.deepcopy(last_fact)
            new_fact['subspace'].pop(i)
            if check_contrast(new_fact, df, schema, last_parameter, method):
                possibleFacts.append(new_fact)
    elif len(last_fact['subspace']) == 1:
        new_fact = copy.deepcopy(last_fact)
        new_fact['subspace'].pop(0)
        if check_contrast(new_fact, df, schema, last_parameter, method):
            possibleFacts.append(new_fact)
    return possibleFacts

def check_contrast(fact, df, schema, parameter, method):
    _, new_parameter, _, _, _ = fact_scoring(fact, df, schema, method)
    if fact['type'] == 'trend':
        # increasing -> decreasing
        return new_parameter != parameter
    elif fact['type'] == 'association':
        return (new_parameter * parameter) < 0

    return False
