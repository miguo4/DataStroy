from .association import association
from .categorization import categorization
from .difference import difference
from .distribution import distribution
from .extreme import extreme
from .outlier import outlier
from .proportion import proportion 
from .rank import rank
from .trend import trend
from .value import value
from .impact import impact_focus, impact_context
from .information import information

def significance(fact, fact_df, subspace_df, focus_df, df, method):
    # print(fact['type'])
    if fact['type'] == 'association':
        return association(fact, fact_df, method)
    elif fact['type'] == 'categorization':
        return categorization(fact, fact_df, method)
    elif fact['type'] == 'difference':
        return difference(fact, fact_df, method)
    elif fact['type'] == 'distribution':
        return distribution(fact, fact_df, method)
    elif fact['type'] == 'extreme':
        return extreme(fact, fact_df, method)
    elif fact['type'] == 'outlier':
        return outlier(fact, fact_df, method)
    elif fact['type'] == 'proportion':
        return proportion(fact, fact_df, method)
    elif fact['type'] == 'rank':
        return rank(fact, fact_df, method)
    elif fact['type'] == 'trend':
        return trend(fact, fact_df, method)
    elif fact['type'] == 'value':
        return value(fact, fact_df, subspace_df, focus_df, df, method)
    else:
        print('not available fact type')
        return 0

__all__ = ['significance', 'impact_focus', 'impact_context', 'information']