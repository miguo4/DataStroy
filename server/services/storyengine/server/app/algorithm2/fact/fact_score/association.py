# Pearson CorrelationCoefficient
from scipy.stats import pearsonr

def association(fact, fact_df, method):

    if method == "nosig":
        return 1, 1

    field1 = fact['measure'][0]['field']
    field2 = fact['measure'][1]['field']
    if (field1 == field2):
        return 0, 1
    else:
        measure_list1 = fact_df[field1]
        measure_list2 = fact_df[field2]
        r_row, p_value = pearsonr(measure_list1,measure_list2)
        # parameter = 'positive' if r_row > 0 else 'negative'
        parameter = r_row
        r_row = abs(r_row)

        return r_row, parameter