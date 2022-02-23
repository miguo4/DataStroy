# Maximum: Significance of Outstanding No. 1 for non-negative value
# Minimum: Significance of Outstanding No. Last for negative value
# According to QuickInsights, we fix β = 0.7 in the power-law fitting
import powerlaw
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import norm

def extreme(fact, fact_df, method):
    measure = fact['measure'][0]['field']
    groupby = fact['groupby'][0]
    measure_list = fact_df[measure].tolist()
    parameter = ['', '0']
    if len(measure_list) <= 2 or len(fact['focus']) != 1:
        return 0, parameter
    focus = fact['focus'][0]['value']
    focus_row = fact_df[fact_df[groupby]==focus]
    if len(focus_row) == 0:
        return 0, parameter
    focus_measure = focus_row.iloc[0][measure]
    parameter[1] = str(focus_measure)
    if method == "nosig":
        return 1, parameter
    if (np.array(measure_list) >= 0).all() or (np.array(measure_list) <= 0).all():
        parameter[0] = 'max'
        if measure_list[0] < 0:
            # Minimum
            parameter[0] = 'min'
            measure_list = list(map(lambda x:-x, measure_list))
        
        # 1. We sort {𝑥} in descending order;
        measure_list.sort(reverse=True)
        if abs(focus_measure) != abs(measure_list[0]):
            parameter[0] = ''
            return 0, parameter
        # 2. We assume the long-tail shape obeys a power-law function. Then we conduct regression analysis for the values in {𝑥}\𝑥 𝑚𝑎𝑥 using power-law functions 𝛼 ∙ 𝑖 −𝛽 , where 𝑖 is an order index and in our current implementation we fix β = 0.7 in the power-law fitting;
        y = measure_list
        indexs = list(map(lambda x: x+1, list(range(len(measure_list)))))
        X = list(map(lambda x: [x**-0.7], indexs))
        reg = LinearRegression().fit(X, y)
        prediction_list = reg.predict(X)
        # 3. We assume the regression residuals obey a Gaussian distribution. Then we use the residuals in the preceding regression analysis to train a Gaussian model 𝐻;
        residual_list = [prediction_list[i] - measure_list[i] for i in range(len(prediction_list))]
        parameters = norm.fit(residual_list)
        # 4. We use the regression model to predict 𝑥 𝑚𝑎𝑥 and get the corresponding residual 𝑅;
        max_residual = residual_list[0]
        cd = norm(parameters[0], parameters[1]).cdf(max_residual)
        # 5. The p-value will be calculated via 𝑃(𝑅|𝐻).
        p = 0
        if np.isnan(cd):
            return p, parameter
        if cd > 0.5:
            p = 2 * (1-cd)
        else:
            p = 2 * cd
        return p, parameter
    else:
        return 0, parameter