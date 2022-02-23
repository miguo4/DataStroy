import math

# A high proportion corresponds to a high score for Proportion.
# It should be leading value that dominates the group
def proportion(fact, fact_df, method):
    measure_field = fact['measure'][0]['field']
    total = fact_df[measure_field].sum()
    if total == 0:
        return 0, '0%'

    focus_field = fact['focus'][0]['field']
    focus_value = fact['focus'][0]['value']
    focus_row = fact_df.loc[fact_df[focus_field] == focus_value]
    if len(focus_row) == 0:
        return 0, '0%'
    if focus_row.shape[0] >=2:
        part = focus_row[measure_field].sum()
    else:
        part = focus_row.iloc[0][measure_field]
    proportion = part/total
    parameter = '%.2f%%'%(proportion*100)
    if method == "nosig":
        return 1, parameter
    
    # Nan : when computing this we want to make sure the filed has multiple values. 
    # A sigle value field may directly lead to 100%
    
    if proportion > 0.5:
        # dominates the group
        return 1, parameter
    else:
        return proportion, parameter

    # return math.sqrt(proportion), parameter