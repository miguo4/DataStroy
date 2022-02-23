import copy
from .helper import filterfields

def getSimilarityPossibleFacts(schema, last_fact):
    n_fields = filterfields(schema, 'numerical')
    c_fields = filterfields(schema, 'categorical')
    t_fields = filterfields(schema, 'temporal')
    g_fields = filterfields(schema, 'geographical')
    ctg_fields = c_fields + t_fields + g_fields
    possibleFacts = []
    # Similarity
    # 1. change measure
    if len(last_fact['measure']) == 0:
        # add all possible fact 
        for field in n_fields:
            new_fact = copy.deepcopy(last_fact)
            new_fact['measure'].append({
                "aggregate": "sum"
            })
            new_fact['measure'][0]['field'] = field['field']
            possibleFacts.append(new_fact)
    else:
        last_measure = last_fact['measure'][0]['field']
        for field in n_fields:
            if last_measure == field['field']:
                continue
            new_fact = copy.deepcopy(last_fact)
            new_fact['measure'][0]['field'] = field['field']
            possibleFacts.append(new_fact)
        
    # 2. change groupby
    facttypes_with_focus = ['outlier', 'proportion', 'extreme', 'difference']
    facttypes_without_focus = ['distribution', 'rank', 'categorization', 'association', 'trend', 'value']
    if len(last_fact['groupby']) > 0:
        last_groupby = last_fact['groupby'][0]
    else:
        last_groupby = ''
    for field in ctg_fields:
        if last_groupby == field['field']:
            continue
        for fact_type in facttypes_without_focus:
            new_fact = copy.deepcopy(last_fact)
            new_fact['type'] = fact_type
            if fact_type == 'categorization':
                new_fact['measure'] = []
            if last_fact['type'] == 'categorization':
                new_fact['measure'] = [{
                    "field": n_fields[0]['field'],
                    "aggregate": "sum"
                }]
            new_fact['groupby'] = [field['field']]
            new_fact['focus'] = []
            possibleFacts.append(new_fact)

    # 3. change categorical filter
    if len(last_fact['subspace']) != 0:
        for index, subspace in enumerate(last_fact['subspace']):
            field = __search_field(schema, field=subspace['field'])
            if field['type'] != 'categorical':
                continue
            if 'values' in field:
                for value in field['values']:
                    if value == subspace['value']:
                        continue
                    else:
                        new_fact = copy.deepcopy(last_fact)
                        new_fact['subspace'][index]['value'] = value
                        possibleFacts.append(new_fact)
    return possibleFacts

def __search_field(schema, field):
    search_field = list(filter(lambda x: (x["field"] == field) , schema['fields']))
    if len(search_field) == 0:
        return None
    else:
        return search_field[0]