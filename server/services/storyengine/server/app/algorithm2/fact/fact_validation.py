from .fact_extraction import fact_extraction

def fact_validation(fact, schema, df):
    # subspace check
    fact_df, _, _ = fact_extraction(fact, df.copy())
    if fact_df.shape[0] == 0:
        #print('0 results')
        return False

    # subspace field equal to groupby
    for subspace in fact['subspace']:
        for groupby_field in fact['groupby']:
            if groupby_field == subspace['field']:
                return False

    # type check
    if fact['type'] == 'distribution':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        # groupby should be categorical
        groupby_field = fact['groupby'][0]
        search_field = list(filter(lambda x: (x["field"] == groupby_field) , schema['fields']))[0]
        if search_field['type'] != 'categorical':
            #print('not categorical in distribution')
            return False
        if len(fact['focus']) != 0:
            #print('wrong focus')
            return False
    elif fact['type'] == 'difference':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        if len(fact['focus']) != 2:
            #print('wrong focus')
            return False
        # groupby should be categorical
        groupby_field = fact['groupby'][0]
        search_field = list(filter(lambda x: (x["field"] == groupby_field) , schema['fields']))[0]
        if search_field['type'] != 'categorical':
            #print('not categorical in difference')
            return False
    elif fact['type'] == 'rank':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        # groupby should be categorical
        groupby_field = fact['groupby'][0]
        search_field = list(filter(lambda x: (x["field"] == groupby_field) , schema['fields']))[0]
        if search_field['type'] != 'categorical':
            #print('not categorical in rank')
            return False
    elif fact['type'] == 'categorization':
        if len(fact['measure']) != 0:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        # groupby should be categorical
        groupby_field = fact['groupby'][0]
        search_field = list(filter(lambda x: (x["field"] == groupby_field) , schema['fields']))[0]
        if search_field['type'] != 'categorical':
            #print('not categorical in categorization')
            return False
        if len(fact['focus']) != 0:
            #print('wrong focus')
            return False
    elif fact['type'] == 'value':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 0:
            #print('wrong groupby')
            return False
        if len(fact['focus']) != 0:
            #print('wrong focus')
            return False
    elif fact['type'] == 'extreme':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        if len(fact['focus']) != 1:
            #print('wrong focus')
            return False
    elif fact['type'] == 'proportion':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        if len(fact['focus']) != 1:
            #print('wrong focus')
            return False
        # groupby should be categorical
        groupby_field = fact['groupby'][0]
        search_field = list(filter(lambda x: (x["field"] == groupby_field) , schema['fields']))[0]
        if search_field['type'] != 'categorical':
            #print('not categorical in proportion')
            return False
    elif fact['type'] == 'outlier':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        if len(fact['focus']) != 1:
            #print('wrong focus')
            return False
    elif fact['type'] == 'association':
        if len(fact['measure']) != 2:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        if len(fact['focus']) != 0:
            #print('wrong focus')
            return False
    elif fact['type'] == 'trend':
        if len(fact['measure']) != 1:
            #print('wrong measure')
            return False
        if len(fact['groupby']) != 1:
            #print('wrong groupby')
            return False
        # groupby should be temporal
        groupby_field = fact['groupby'][0]
        search_field = list(filter(lambda x: (x["field"] == groupby_field) , schema['fields']))[0]
        if search_field['type'] != 'temporal':
            #print('not temporal in trend')
            return False
        if len(fact['focus']) != 0:
            #print('wrong focus')
            return False
    else:
        #print('wrong type')
        return False

    return True

