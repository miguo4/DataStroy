import copy
from .helper import filterfields
from ..fact import fact_scoring, fact_validation, fact_extraction, fact_focus

def getElaborationPossibleFacts(df, schema, last_fact):
    c_fields = filterfields(schema, 'categorical')
    t_fields = filterfields(schema, 'temporal')
    g_fields = filterfields(schema, 'geographical')
    ctg_fields = c_fields + t_fields + g_fields
    possibleFacts = []
    # Elaboration
    facttypes_with_focus = ['outlier', 'proportion', 'extreme', 'difference']
    facttypes_without_focus = ['distribution', 'rank', 'categorization', 'association', 'trend', 'value']
    # 1. change type add focus
    if len(last_fact['focus']) == 0 and len(last_fact['groupby']) > 0:
        for fact_type in facttypes_with_focus:
            new_fact = copy.deepcopy(last_fact)
            new_fact['type'] = fact_type
            fact_df,_,_ = fact_extraction(new_fact, df)
            new_fact = fact_focus(new_fact, fact_df)
            # check outlier
            if fact_type == 'outlier':
                if not fact_validation(new_fact, schema, df):
                    continue
                score, _, _, _, _ = fact_scoring(new_fact, df, schema)
                if score == 0:
                    continue
            possibleFacts.append(new_fact)

    # 2. add filter
    if last_fact['type'] in facttypes_without_focus:
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
                        possibleFacts.append(new_fact)

    return possibleFacts