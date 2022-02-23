# Value fact only derive values from the data. We simply assign it to zero.
# or
# score（value) = P(subspace) * P(value|subspace)
# P(value|subspace) = 1/5 （sum/avg/max/min/count）
def value(fact, fact_df, subspace_df, focus_df, df, method):
    
    subspace_df=subspace_df.reset_index(drop=True)

    P_subspace = len(subspace_df)/len(df)
    score = 0.2 * P_subspace
    subspace_df['COUNT'] = 1
    field = fact['measure'][0]['field']
    aggregation = "sum"
    # aggregation = fact['measure'][0]['aggregate']
    if aggregation == 'avg':
        aggregation = 'mean'
    parameter = 0
    if aggregation == '':
        agg_df = subspace_df[field][0]
    elif aggregation == 'count':
        agg_df = subspace_df.agg({'COUNT':'count'})
    else:
        agg_df = subspace_df.agg({field:aggregation})
    parameter = float(agg_df)
    if method == "nosig":
        return 1, parameter
    return score, parameter