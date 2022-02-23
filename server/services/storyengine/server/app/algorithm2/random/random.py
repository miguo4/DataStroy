import copy
import random
import datetime
import multiprocessing
import numpy as np
from .helper import filterfields
from ..fact import fact_scoring, fact_validation, fact_extraction, fact_focus

class RandomGenerator:
    def __init__(self, df, schema):
        self.df = df
        self.schema = schema
        self.processLock = multiprocessing.Lock()
        self.manager = multiprocessing.Manager()
        self.generatedFacts = self.manager.list()
        # self.random_policy = random.choice(['measure', 'subspace']) # measure or subspace
        self.random_policy = random.choice(['measure'])
        print('#################################')
        print('current random policy: %s'%(self.random_policy))
        self.pool = {} # cache fact importance score

        # columns
        self.n_fields = filterfields(schema, 'numerical')
        self.c_fields = filterfields(schema, 'categorical')
        self.t_fields = filterfields(schema, 'temporal')
        self.g_fields = filterfields(schema, 'geographical')
        self.cg_fields = self.c_fields + self.g_fields
        self.ctg_fields = self.c_fields + self.t_fields + self.g_fields
        # enumarate measure
        self.measure_list = []
        for n_field in self.n_fields:
            self.measure_list.append([{'field': n_field['field'],'aggregate': 'sum'}])
            self.measure_list.append([{'field': n_field['field'],'aggregate': 'avg'}])
            # self.measure_list.append([{'field': n_field['field'],'aggregate': 'max'}])
            # self.measure_list.append([{'field': n_field['field'],'aggregate': 'min'}])
        self.selected_measure = random.choice(self.measure_list)
        if self.random_policy == 'measure':
            print('#################################')
            print('selected measure: %s'%(self.selected_measure[0]['field']))
            print('#################################')
        

        # enumarate subspace
        self.subspace_list = []
        self.subspace_list.append([])
        for field in self.ctg_fields:
            if 'values' in field:
                for value in field['values']:
                    self.subspace_list.append([{'field':field['field'], 'value':value}])
        self.selected_subspace = random.choice(self.subspace_list)
        if self.random_policy == 'subspace':
            print('#################################')
            print('selected subspace: %s'%(self.selected_subspace))
            print('#################################')

    # 
    # Generate
    # 
    def generate(self):
        self.generateByParallel()
        if len(self.generatedFacts) == 0 and self.random_policy == 'subspace':
            self.random_policy = 'measure'
            print('#################################')
            print('failed to generate in selected subspace: %s'%(self.selected_subspace))
            print('#################################')
            print('switch to random policy: %s'%(self.random_policy))
            print('#################################')
            print('selected measure: %s'%(self.selected_measure[0]['field']))
            print('#################################')
            self.generateByParallel()
        return self.generatedFacts

    # 
    # Create facts in parallel processes
    # 
    def generateByParallel(self):
        process_list = []
        for column in self.ctg_fields:
            columnfield = column['field']
            process_list.append(multiprocessing.Process(target=self.generateRandomly, args=(columnfield, 1000, )))
        for process in process_list:
            process.start()
        for process in process_list:
            process.join()

    # 
    # Create a set of facts randomly
    # 
    def generateRandomly(self, columnfield, scale=1000):
        candidates = []
        for _ in range(scale):
            try:
                candidates.append(self.generateByColumn(columnfield))
            except:
                print(self.generateByColumn(columnfield))
                continue
        candidates = list(filter(lambda x: self._validate(x), candidates)) # validation
        candidates = list(map(lambda x: self._calculate(x), candidates)) # score calulation
        candidates = list(filter(lambda x: x['significance']>0.05, candidates)) # filter low significance
        candidates.sort(reverse=True, key=lambda x: x['significance'])
        self.processLock.acquire()
        print('add %s random facts in %s'%(len(candidates),columnfield))
        self.generatedFacts += candidates
        self.processLock.release()
        return candidates

    # 
    # Create a random fact by column
    # 
    def generateByColumn(self, columnfield):
        # enumarate subspace
        column_subspace_list = []
        column_subspace_list.append([])
        if self.random_policy == 'subspace':
            column_subspace_list = [self.selected_subspace]
        else:
            for field in self.ctg_fields:
                if field['field'] != columnfield:
                    continue
                elif 'values' in field:
                    for value in field['values']:
                        column_subspace_list.append([{'field':field['field'], 'value':value}])

        facttypes = ['outlier', 'proportion', 'extreme', 'difference','distribution', 'rank', 'categorization', 'trend', 'value']
        facttype = random.choice(facttypes)
        return self.generateByType(facttype, column_subspace_list)

    # 
    # Create a set of facts randomly by type
    # 
    def generateByType(self, facttype, subspace_list = []):
        if len(subspace_list) == 0:
            subspace_list = self.subspace_list
        facttypes_with_focus = ['outlier', 'proportion', 'extreme', 'difference']
        facttypes_without_focus = ['distribution', 'rank', 'categorization', 'association', 'trend', 'value']

        new_fact = {
            "type": facttype,
            "measure": [],
            "subspace": [],
            "groupby": [],
            "focus": []
        }

        # add measure
        if self.random_policy == 'measure':
            new_fact['measure'] = self.selected_measure
        else:
            new_fact['measure'] = random.choice(self.measure_list)
        
        # add subspace
        new_fact['subspace'] = random.choice(subspace_list)

        # add groupby
        if facttype == 'trend':
            new_fact['groupby'] = [random.choice(self.t_fields)['field']] if len(self.t_fields) > 0 else []
        elif facttype in ['categorization', 'distribution']:
            new_fact['groupby'] = [random.choice(self.cg_fields)['field']] if len(self.cg_fields) > 0 else []
        elif facttype == 'value':
            new_fact['groupby'] = []
        else:
            new_fact['groupby'] = [random.choice(self.ctg_fields)['field']] if len(self.ctg_fields) > 0 else []

        # add focus
        if facttype in facttypes_with_focus:
            fact_df,_,_ = fact_extraction(new_fact, self.df)
            try:
                new_fact = fact_focus(new_fact, fact_df)
            except:
                # print('focus error')
                pass
            

        return self._jsonify(new_fact)

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
            fact_score, fact_parameter, fact_possibility, fact_information, fact_significance = fact_scoring(fact, self.df, self.schema)
            fact['score'] = fact_score
            fact['parameter'] = fact_parameter
            fact['possibility'] = fact_possibility
            fact['information'] = fact_information
            fact['significance'] = fact_significance
            self.pool[factid] = fact # add to pool
            return fact

    def _jsonify(self, fact):
        for i, focus in enumerate(fact['focus']):
            if isinstance(focus['value'], int) or isinstance(focus['value'], float):
                fact['focus'][i]['value'] = str(fact['focus'][i]['value'])
            elif isinstance(focus['value'], datetime.datetime) or not isinstance(focus['value'], str):
                date_text = str(focus['value'])[:10]
                date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                fact['focus'][i]['value'] = date.strftime('%Y/%m/%d')
        for i, subspace in enumerate(fact['subspace']):
            if isinstance(subspace['value'], int) or isinstance(subspace['value'], float):
                fact['subspace'][i]['value'] = str(fact['subspace'][i]['value'])
            elif isinstance(subspace['value'], datetime.datetime) or not isinstance(subspace['value'], str):
                date_text = str(subspace['value'])[:10]
                date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                fact['subspace'][i]['value'] = date.strftime('%Y/%m/%d')
        return fact