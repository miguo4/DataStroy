import traceback

def difference(fact, fact_df, method):
    measure_field = fact['measure'][0]['field']
    focus_field = fact['focus'][0]['field']
    focus1 = fact['focus'][0]['value']
    focus2 = fact['focus'][1]['value']

    if focus1 == focus2 :
        return 0, 0
    try:
        focus1_df = fact_df.loc[fact_df[focus_field]==focus1]
        if len(focus1_df) == 0:
            return 0, 0
        
        # print(focus1_df[measure_field].item())
        focus1_value = focus1_df[measure_field].values.item()
    
        focus2_df = fact_df.loc[fact_df[focus_field]==focus2]
        if len(focus2_df) == 0:
            return 0, 0
        focus2_value = focus2_df[measure_field].values.item()

        _max = fact_df[measure_field].max()
        _min = fact_df[measure_field].min()
        max_diff = _max - _min
        if max_diff == 0:
            return 0,0
        # max - min is 1 and self - self is 0, p=[0,1]
        p = abs(focus1_value - focus2_value) / max_diff
        parameter = abs(focus1_value - focus2_value)
        if method == "nosig":
            return 1, parameter
        return p, parameter

    except Exception as e:
        print(traceback.format_exc())
        # this bug is becasue we focused on a field that has multiple values,
        # which is actually an invalidate fact
        # print('########################')
        # print(focus1)
        # print(focus2)
        # print(focus_field)
        # print(measure_field)
        # print(focus1_df)
        # print('########################')
        return 0, 0