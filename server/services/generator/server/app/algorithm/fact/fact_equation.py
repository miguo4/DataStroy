def fact_equation(fact1, fact2):
    # if fact1['type'] != fact2['type']:
    #     return False
    if set(list(map(lambda x: x["field"], fact1['measure']))) != set(list(map(lambda x: x["field"], fact2['measure']))):
        return False
    if set(fact1['groupby']) != set(fact2['groupby']):
        return False
    if set(list(map(lambda x: "%s++%s"%(x["field"],x["value"]), fact1['subspace']))) != set(list(map(lambda x: "%s++%s"%(x["field"],x["value"]), fact2['subspace']))):
        return False
    if set(list(map(lambda x: "%s++%s"%(x["field"],x["value"]), fact1['focus']))) != set(list(map(lambda x: "%s++%s"%(x["field"],x["value"]), fact2['focus']))):
        return False
    return True