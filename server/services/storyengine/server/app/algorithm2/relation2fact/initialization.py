import copy
import numpy as np
from .helper import filterfields

def getInitialFacts(schema):
    n_fields = filterfields(schema, 'numerical')
    c_fields = filterfields(schema, 'categorical')
    t_fields = filterfields(schema, 'temporal')
    g_fields = filterfields(schema, 'geographical')
    cg_fields = c_fields + g_fields
    possibleFacts = []

    # Trend
    trendFacts = []
    if len(t_fields) > 0:
        # Trend
        trend_fact = {
            "type": "trend",
            "measure": [],
            "subspace": [
            ],
            "groupby": [],
            "focus": []
        }
        for t_field in t_fields:
            for n_field in n_fields:
                new_fact = copy.deepcopy(trend_fact)
                new_fact['measure'] = [
                    {
                        'field': n_field['field'],
                        'aggregate': 'sum',
                    }
                ]
                new_fact['groupby'] = [t_field['field']]
                trendFacts.append(new_fact)

    # Value
    valueFacts = []
    if len(n_fields) > 0:
        # Value
        value_fact = {
            "type": "value",
            "measure": [],
            "subspace": [
            ],
            "groupby": [],
            "focus": []
        }
        for n_field in n_fields:
            new_fact = copy.deepcopy(value_fact)
            new_fact['measure'] = [
                {
                    'field': n_field['field'],
                    'aggregate': 'sum',
                }
            ]
            valueFacts.append(new_fact)

    # Categorozization
    categorizationFacts = []
    if len(cg_fields) > 0:
        # categorization
        cat_fact = {
            "type": "categorization",
            "measure": [],
            "subspace": [
            ],
            "groupby": [],
            "focus": []
        }
        for c_field in cg_fields:
            new_fact = copy.deepcopy(cat_fact)
            new_fact['groupby'] = [c_field['field']]
            categorizationFacts.append(new_fact)

    possibleFacts = trendFacts + valueFacts + categorizationFacts

    return possibleFacts