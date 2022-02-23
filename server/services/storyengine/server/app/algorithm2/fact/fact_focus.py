def fact_focus(fact, fact_df):
    facttypes_with_focus = ['outlier', 'proportion', 'extreme', 'difference']
    facttypes_without_focus = ['distribution', 'rank', 'categorization', 'association', 'trend', 'value']\

    if len(fact['groupby']) == 0:
        return fact

    if fact['type'] in facttypes_without_focus:
        fact['focus'] = []
        
    elif len(fact['measure']) > 0:
        measure_field = fact['measure'][0]['field']
        group_field = fact['groupby'][0]
        max_row = fact_df[fact_df[measure_field] == fact_df[measure_field].max()]
        min_row = fact_df[fact_df[measure_field] == fact_df[measure_field].min()]
        if fact['type'] == 'difference':
            fact['focus'] = [
                {
                    "field": group_field,
                    "value": max_row.iloc[0][group_field]
                },
                {
                    "field": group_field,
                    "value": min_row.iloc[0][group_field]
                }
            ]
        elif fact['type'] == 'extreme':
            if abs(max_row.iloc[0][measure_field]) >= abs(min_row.iloc[0][measure_field]):
                fact['focus'] = [
                    {
                        "field": group_field,
                        "value": max_row.iloc[0][group_field]
                    }
                ]
            else:
                fact['focus'] = [
                    {
                        "field": group_field,
                        "value": min_row.iloc[0][group_field]
                    }
                ]
        elif fact['type'] == 'proportion':
            fact['focus'] = [
                {
                    "field": group_field,
                    "value": max_row.iloc[0][group_field]
                }
            ]
        elif fact['type'] == 'outlier':
            #TODO: detect outlier
            fact['focus'] = [
                {
                    "field": group_field,
                    "value": max_row.iloc[0][group_field]
                }
            ]
    return fact