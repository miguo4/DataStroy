import pandas as pd
import json
import copy

def fact_extraction(fact, df):
    # get subspace
    subspace_df = df.copy()
    for index,subspace in enumerate(fact['subspace']):
        subspace_df = subspace_df[subspace_df[subspace['field']] == subspace['value']]
    focus_df = subspace_df.iloc[0:0]
    for focus in fact['focus']:
        focus_df = focus_df.append(subspace_df[subspace_df[focus['field']] == focus['value']])
    measures = list(map(lambda x:x['field'], fact['measure']))
    measures = list(filter(lambda x:x != 'COUNT', measures))
    groupbys = fact['groupby']
    measure_df = subspace_df[measures+groupbys].copy()
    # aggregation
    # print(fact['measure'])
    if len(groupbys) == 0:
        fact_df = measure_df
        return fact_df, subspace_df, focus_df
    
    measure_df['COUNT'] = 1
    if len(measures) == 0:
        fact_df = measure_df.groupby(fact['groupby'], as_index=False).agg({'COUNT':'count'})
    elif len(measures) == 1:
        if 'aggregate' in fact['measure'][0]:
            aggregation = fact['measure'][0]['aggregate']
            if aggregation == 'avg':
                aggregation = 'mean'
            fact_df = measure_df.groupby(fact['groupby'], as_index=False).agg({fact['measure'][0]['field']:aggregation, 'COUNT':'count'})
        else:
            fact_df = measure_df
    elif len(measures) == 2:
        if 'aggregate' in fact['measure'][0] and 'aggregate' in fact['measure'][1]:
            aggregation0 = fact['measure'][0]['aggregate']
            if aggregation0 == 'avg':
                aggregation0 = 'mean'
            aggregation1 = fact['measure'][1]['aggregate']
            if aggregation1 == 'avg':
                aggregation1 = 'mean'
            fact_df = measure_df.groupby(fact['groupby'], as_index=False).agg({fact['measure'][0]['field']:aggregation0, fact['measure'][1]['field']:aggregation1, 'COUNT':'count'})
        else:
            fact_df = measure_df
        
    return fact_df, subspace_df, focus_df