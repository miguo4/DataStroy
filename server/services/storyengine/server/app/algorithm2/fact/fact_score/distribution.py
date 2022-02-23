from scipy import stats

def distribution(fact, fact_df, method):
    # scipy.stats.normaltest
    # Test whether a sample differs from a normal distribution.
    # scipy.stats.shapiro
    # Perform the Shapiro-Wilk test for normality.
    # NOTE: normaltest cannot have less than 8 sample, shapiro have no restrict. But shapiro does not perform well if #sample > 5000 
    # so PICK shapiro
    measure_field = fact['measure'][0]['field']
    parameter = ''
    if method == "nosig":
        return 1, parameter
    if len(fact_df[measure_field]) < 3:
        return 0, parameter
    else:
        k2, p = stats.shapiro(fact_df[measure_field])
        # the larger likelihood of norm, the less importance.
        return 1-p, parameter