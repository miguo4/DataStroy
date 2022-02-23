import pandas as pd
import math
import json
from .fact_score import significance, impact_context, impact_focus, information
from .fact_extraction import fact_extraction

def fact_scoring(fact, df, schema, method="sig"):
    # get dataframe
    fact_df, subspace_df, focus_df = fact_extraction(fact, df)

    # Fact Significance
    score_significance, fact_parameter = significance(fact, fact_df, subspace_df, focus_df, df, method)
    # print("Fact Significance:%s"%(score_significance))

    fact_information, fact_possibility = information(fact, subspace_df, focus_df, df, schema)
    # print("Information Entropy:%s"%(fact_information))
    # print("Fact Possibility:%s"%(fact_possibility))

    score = score_significance * fact_information
    # print("Importance Score:%s"%(score))

    return score, fact_parameter, fact_possibility, fact_information, score_significance
