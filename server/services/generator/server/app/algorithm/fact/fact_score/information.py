import math
from itertools import combinations

def information(fact, subspace_df, focus_df, df, schema):

    if len(subspace_df) == 0:
        return 0, 0

    # P(subspace)  =  P(field = K) = \frac{1}{C(k, 0) + C(k, 1) + C(k, 2)}*\prod_{i=1}^{k}\frac{{field}_i 上取值为 K_i 的数据的个数}{数据的总数}
    # 其中k表示数据中Categorical的列数，subspace只考虑最多取2列的情况。当subspace包含多个field时，它们各自的取值是相互独立的，所以这里为各自概率的乘积。
    k = schema['statistics']['column'] - schema['statistics']['numerical']
    klist = list(range(0,k))
    # c = 1 + len(list(combinations(klist, 1))) + len(list(combinations(klist, 2)))
    c = 0
    for i in range(0,k+1):
        c += len(list(combinations(klist, i)))
    if len(fact['subspace']) == 0:
        P_subspace = 1 / c
    elif len(fact['subspace']) == 1:
        P_subspace = (1 / c) * len(subspace_df)/len(df)
    elif len(fact['subspace']) == 2:
        subspace1_field = fact['subspace'][0]['field']
        subspace1_value = fact['subspace'][0]['value']
        subspace1_df = df[df[subspace1_field]==subspace1_value]
        subspace2_field = fact['subspace'][1]['field']
        subspace2_value = fact['subspace'][1]['value']
        subspace2_df = df[df[subspace2_field]==subspace2_value]
        P_subspace = (1 / c) * (len(subspace1_df)/len(df)) * (len(subspace2_df)/len(df))
    else:
        P_subspace = 0
        # not support subspace with more than 2 fields
        return 0, 0

    # P(X |subspace) =  P（focus = X | subspace）=   \frac{数据中focus取值为 X 的情况的数目}{subspace 中包含的数据总条目}
    P_focus_subspace = 1
    if len(focus_df) > 0:
        P_focus_subspace = len(focus_df)/len(subspace_df)

    P = P_subspace * P_focus_subspace
    

    # I = - math.log(P, 2)
    try:
        I = - math.log(P, 2)
    except:
        print("An exception occurred")
        return 0, 0

    return I, P