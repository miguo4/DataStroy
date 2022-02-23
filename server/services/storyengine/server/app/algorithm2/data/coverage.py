def check_coverage(facts, schema, df):
    n = schema['statistics']['row']
    fields = schema['fields']
    column_dict = {}
    for field in fields:
        field_name = field['field']
        field_type = field['type']
        column_dict[field_name] = []

    for fact in facts:
        rows = list(range(0,n))
        for subspace in fact['subspace']:
            subspace_field = subspace['field']
            subspace_value = subspace['value']
            subspace_rows = df.index[df[subspace_field] == subspace_value].tolist()
            rows = list(set(rows).intersection(set(subspace_rows))) # get intersection
        for measure in fact['measure']:
            measure_field = measure['field']
            measure_agg = measure['aggregate']
            if measure_agg == 'count':
                continue
            column_dict[measure_field] = list(set(column_dict[measure_field]).union(set(rows))) # get union
        for subspace in fact['subspace']:
            subspace_field = subspace['field']
            column_dict[subspace_field] = list(set(column_dict[subspace_field]).union(set(rows))) # get union
        for groupby in fact['groupby']:
            groupby_field = groupby
            column_dict[groupby_field] = list(set(column_dict[groupby_field]).union(set(rows))) # get union

    coverage = 0
    for field in column_dict:
        column_dict[field] = len(column_dict[field])/n
        coverage += column_dict[field]/len(column_dict)
    # print(column_dict)

    return coverage
