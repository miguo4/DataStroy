import copy
from .helper import filterfields

def getTemporalPossibleFacts(schema, last_fact):
    possibleFacts = []
    # Temporal
    # change temporal filter
    if len(last_fact['subspace']) != 0:
        for index, subspace in enumerate(last_fact['subspace']):
            field = __search_field(schema, field=subspace['field'])
            if field['type'] != 'temporal':
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