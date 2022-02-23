# Evenness: counts for each category are close to each other
# Using CHI square testing
from scipy import stats
import numpy as np
import math

def categorization(fact, fact_df, method):
    if len(fact['measure']) > 0:
        count_list = fact_df[fact['measure'][0]['field']].tolist()
    else:
        count_list = fact_df['COUNT'].tolist()
    count_list.sort()
    N = len(count_list)
    parameter = fact_df[fact['groupby'][0]].tolist() # category list
    if method == "nosig":
        return 1, parameter

    # if the count if category is more than 12 or the group is temperal, it is not suitable for categorization
    if N > 12 or fact_df[fact['groupby'][0]].dtype == 'datetime64[ns]':
        if fact_df[fact['groupby'][0]].dtype == 'datetime64[ns]':
            parameter = list(map(lambda x:x.strftime("%Y/%m/%d"), parameter))
        return 0, parameter

    # Assume: possibilities in each category are equal
    observed = np.array(count_list)
    # print(observed)
    expected = np.array([1 / N] * N) * np.sum(observed)
    # print(expected)

    (t , p) = stats.chisquare(observed, expected, ddof=1)

    if math.isnan(p) or p < 0.001:
        p = 0
    
    return p, parameter