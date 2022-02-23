def fact_focus(fact, fact_df):
    facttypes_with_focus = ['outlier', 'proportion', 'extreme', 'difference']
    facttypes_without_focus = ['distribution', 'rank', 'categorization', 'association', 'trend', 'value']\

    if len(fact['breakdown']) == 0:
        return fact['focus']

    if fact['type'] in facttypes_without_focus:
        fact['focus'] = []
        
    elif len(fact['measure']) > 0:
        measure_field = fact['measure'][0]['field']
        group_field = fact['breakdown'][0]['field']
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
            try:
                value = max_row.iloc[0][group_field].strftime("%Y/%m/%d")
            except:
                value = max_row.iloc[0][group_field]

            fact['focus'] = [
                {
                    "field": group_field,
                    "value": value
                }
                # },
                # {
                #     "field": group_field,
                #     "value": str(min_row.iloc[0][group_field])
                # }
            ]
        elif fact['type'] == 'proportion':
            fact['focus'] = [
                {
                    "field": group_field,
                    "value": max_row.iloc[0][group_field]
                }
            ]
        elif fact['type'] == 'outlier':
            try:
                value = max_row.iloc[0][group_field].strftime("%Y/%m/%d")
            except:
                value = max_row.iloc[0][group_field]

            fact['focus'] = [
                {
                    "field": group_field,
                    "value": value
                }
            ]
            
    return fact['focus']