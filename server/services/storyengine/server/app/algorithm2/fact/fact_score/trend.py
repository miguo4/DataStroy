# a sharp increase corresponds to a high score for Trend.
from scipy.stats import linregress
from pandas import to_datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import logistic


def trend(fact, fact_df, method):
    if method == "nosig":
        return 1, "no trend"
    measure_list = fact_df[fact['measure'][0]['field']].tolist()
    temporal = fact_df[fact['groupby'][0]]
    # 这里默认了数据顺序是由小到大的
    # TODO:要sort temporal 
    # print('fact:%s'%(fact))
    # print(temporal)

    if (len(temporal) <= 3):
        return 0, 'no trend'
    else:
        temporal = (temporal-temporal.min())/(temporal.max()-temporal.min())
        temporalIndex = temporal*(len(temporal) - 1)
        # temporalIndex = list(range(len(temporal)))

        # 造数据
        # 1. slope -0.4 emission数据 拟合的比较好 sig中等
        # 2. slope大
        # measure_list = [10, 100, 200,300,400,500]
        # temporalIndex = [2001,2002,2003,2004,2005,2006]
        # 3. slope小 拟合程度也不好
        # measure_list = [110, 0, 200,-100,100,-100]
        # temporalIndex = [2001,2002,2003,2004,2005,2006]


        # print('measure_list:')
        # print(measure_list)
        # print('temporalIndex:')
        # print(temporalIndex)

        X = np.array(temporalIndex).reshape(-1,1)
        y = measure_list
        reg = LinearRegression()
        reg.fit(X,y)

        # r^2
        r2 = reg.score(X, y)
        if r2 < 0:
            r2 = 0
        # print("r^2 = %f"%(r2))

        # slope
        slope = reg.coef_[0]
        # print("slope = %f"%(slope))

        # TODO: 与检验数据相差结果
        # slopeA = 1.02, topk结果是0.11, 我的结果是0.08
        # slopeB = 0.11, topk结果是0.79, 我的结果是0.83

        vals = logistic.cdf(slope, loc = 0,scale = 0.32)
        # 如果slope大于0，则面积 = (1 - vals) * 2
        # 如果slope小于0，则面积 = vals * 2
        
        if(slope >= 0): 
            p = (1 - vals) * 2
        else:
            p = vals * 2
        # print("p-value = %f"%(p))
        
        sig = r2 * (1 - p)
        # print("sig = %f"%(sig))
        # print("__________________________________")
        parameter = 'increasing' if slope >= 0 else 'decreasing'
        return sig, parameter