import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats

def rank(fact, fact_df, method):
    measure_list = fact_df[fact['measure'][0]['field']].tolist()
    measure_list.sort(reverse=True)
    fact_df = fact_df.sort_values(fact['measure'][0]['field'], ascending=False )
    parameter = fact_df[fact['groupby'][0]].tolist()
    if fact_df[fact['groupby'][0]].dtype == 'datetime64[ns]':
        parameter = list(map(lambda x:x.strftime("%Y/%m/%d"), parameter))
    # measure_list =[10, 6, 3, 2.5, 2.4, 2.3, 2.0, 1.8, 1.8, 1.8]
    # measure_list = [10 * i ** -0.7 for i in range(1, 10)]
    # measure_list = [1,2,3,4,5,6,7,8,9]
    if len(measure_list) == 0: # no measure
        return 0, parameter
    if measure_list[0] / np.sum(measure_list) > 0.5: # if dominate
        return 0, parameter
    if len(list(filter(lambda x: (x < 0), measure_list))) > 0 and len(list(filter(lambda x: (x < 0), measure_list)))!= len(measure_list): # both pos and neg
        return 0, parameter
    if method == "nosig":
        return 1, parameter
    # abs all value in the measure_list
    measure_list = list(map(abs, measure_list))
    y = measure_list
    X = list(map(lambda x: [(x+1)**-0.7], list(range(len(measure_list)))))
    # using linear regression to fit power law distribution. fit_intercept=False means y=ax, no b
    reg = LinearRegression(fit_intercept=False).fit(X, y)
    # using the R2 score of the model as the significance of the rank distribution, ->1 means the rank is like the power law, which is we wanted.
    # R2 score range [-, 1], if R2 < 0 return 0.
    p = reg.score(X,y) if reg.score(X,y) > 0 else 0

    return p, parameter