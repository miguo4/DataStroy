from .fact import fact_scoring, fact_validation
from .relation2fact import getSimilarityPossibleFacts, getContrastPossibleFacts, getCauseEffectPossibleFacts, getTemporalPossibleFacts, getElaborationPossibleFacts, getGeneralizationPossibleFacts, getInitialFacts

class FactFactory:
    def __init__(self, df, schema, method="sig"):
        self.pool = {}
        self.df = df
        self.schema = schema
        self.method = method

    # 
    # Create a set of #number facts according to a reference fact (#ref) and a given relation (#rel)
    # 
    def createByLogic(self, ref, rel):
        candidates = []

        # similarity
        if rel == 'similarity': 
            candidates = getSimilarityPossibleFacts(self.schema, ref)
        # temporal
        elif rel == 'temporal':
            candidates = getTemporalPossibleFacts(self.schema, ref)
        # contrast
        elif rel == 'contrast':
            candidates = getContrastPossibleFacts(self.df, self.schema, self.method, ref)
        # cause-effect
        elif rel == 'cause-effect':
            candidates = getCauseEffectPossibleFacts(self.df, self.schema, ref)
        # elaboration
        elif rel == 'elaboration':
            candidates = getElaborationPossibleFacts(self.df, self.schema, ref)
        # generalization
        elif rel == 'generalization':
            candidates = getGeneralizationPossibleFacts(self.schema, ref)

        candidates = list(filter(lambda x: self._validate(x), candidates)) # validation
        candidates = list(map(lambda x: self._calculate(x), candidates)) # score calulation
        candidates = list(filter(lambda x: x['significance']>0.05, candidates)) # filter low significance

        return candidates

    # 
    # Create a set of #number initial facts
    # 
    def createByInitialation(self):
        candidates = getInitialFacts(self.schema)
        candidates = list(filter(lambda x: self._validate(x), candidates)) # validation
        candidates = list(map(lambda x: self._calculate(x), candidates)) # score calulation
        candidates = list(filter(lambda x: x['significance']>0.05, candidates)) # filter low significance
        return candidates

    def _validate(self, fact):
        if fact_validation(fact, self.schema, self.df):
            return True
        else:
            return False

    def _calculate(self, fact):
        factid = hash(str(fact))
        if factid in self.pool:
            return self.pool[factid]
        else:
            fact_score, fact_parameter, fact_possibility, fact_information, fact_significance = fact_scoring(fact, self.df, self.schema, self.method)
            fact['score'] = fact_score
            fact['parameter'] = fact_parameter
            fact['possibility'] = fact_possibility
            fact['information'] = fact_information
            fact['significance'] = fact_significance
            self.pool[factid] = fact # add to pool
            return fact

    def _filterfields(self, dtype):
        if self.schema['statistics'][dtype] == 0:
            return []
        else:
            return list(filter(lambda x: (x["type"] == dtype) , self.schema['fields']))