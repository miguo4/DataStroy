import numpy as np
from scipy.stats import zscore
from scipy.stats import norm

def isArraySame(array):
    i= 0
    a = list(array)
    while i < len(a):
        if(a[i] != a[0]):
            return False
        i += 1

    return True

def outlier(fact, fact_df, method):
    # print('--------------------------------------------')
    fact_df = fact_df.sort_values(fact['measure'][0]['field'], ascending=True )
    measure_field = fact['measure'][0]['field']
    measure_data = fact_df[measure_field]
    # 造数据
    # measure_data = np.array([0,0,0,0,0,100])
    # print(isArraySame(measure_data))
    rows = fact_df.loc[fact_df[fact['focus'][0]['field']] == fact['focus'][0]['value']]
    if len(rows) == 0:
        return 0, 0

    parameter = float(rows.iloc[0][measure_field])
    
    # 利用四分位法判断是否存在outlier
    Ser = measure_data
    Low = Ser.quantile(0.25)-1.5*(Ser.quantile(0.75)-Ser.quantile(0.25))
    Up = Ser.quantile(0.75)+1.5*(Ser.quantile(0.75)-Ser.quantile(0.25))
    index = (Ser< Low) | (Ser>Up)
    Outlier = Ser.loc[index]
    if method == "nosig":
        return 1, parameter
    if(len(Outlier) == 0):
        return 0, parameter

    # to remove
    # return 0, parameter
    if(len(measure_data) == 0 or isArraySame(measure_data)):
        return 0, parameter
    else:  
        # print(zscore(measure_data))
        outlier = abs(zscore(measure_data))
        # print(outlier.max())
        parameters = norm.fit(zscore(measure_data))
        # cd = norm(parameters[0], parameters[1]).cdf(outlier.max())
        p_value = norm(parameters[0], parameters[1]).sf(outlier.max())*2
        # print("p_value = %f"%(p_value))
        sig = 1 - p_value
        # print("sig = %f"%(sig))
        # print('--------------------------------------------')
        return sig, parameter