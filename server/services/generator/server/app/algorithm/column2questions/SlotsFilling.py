import re
import random
from functools import reduce

class SlotsFilling:
    def __init__(self):
        self.__canadiate_slots = {}
        self.__schema={}

    def load(self, schema): # table_schema <----> template_slots
        self.__schema=schema
        categorical_columns=[x['field'] for x in self.__schema['fields'] if x['type']=='categorical']
        temporal_columns=[x['field'] for x in self.__schema['fields'] if x['type']=='temporal']
        numerical_columns=[x['field'] for x in self.__schema['fields'] if x['type']=='numerical']
        geographical_columns=[x['field'] for x in self.__schema['fields'] if x['type']=='geographical']
        categorical_values=[x['values'] for x in self.__schema['fields'] if x['type']=='categorical']
        temporal_values=[x['values'] for x in self.__schema['fields'] if x['type']=='temporal']
        geographical_values=[x['values'] for x in self.__schema['fields'] if x['type']=='geographical']
        canadiate_slots={
            'breakdown_G':geographical_columns,
            'breakdown_C':categorical_columns,
            'breakdown_T':temporal_columns,
            'measure':numerical_columns,
            'subspace_C':categorical_values,
            'subspace_G':geographical_values,
            'subspace_T':temporal_values,
            'focus':[]
        }
        
        if len(temporal_values)!=0:
            canadiate_slots['subspace_T'] = list(reduce(lambda x,y:x+y, temporal_values))
        else:
            canadiate_slots.pop('breakdown_T')
            canadiate_slots.pop('subspace_T')

        if len(categorical_values)!=0:
            canadiate_slots['subspace_C'] = list(reduce(lambda x,y:x+y, categorical_values))
        else:
            canadiate_slots.pop('breakdown_C')
            canadiate_slots.pop('subspace_C')

        
        if len(geographical_values)!=0:
            canadiate_slots['subspace_G'] = list(reduce(lambda x,y:x+y, geographical_values))
        else:
            canadiate_slots.pop('breakdown_G')
            canadiate_slots.pop('subspace_G')

        # print(canadiate_slots)
        self.__canadiate_slots=canadiate_slots

    def slotsfilling_from_template(self,simple): # input a template and canadiate_slots, return corpus
        template=simple['modified questions']
        slots=re.findall('<[^<>]*>',template)
        slots1=re.findall('<([^<>]*)>',template)
        if len(slots1)!=0:
            filled_slots=[]
            for slot in slots1:
                if slot == 'focus':
                    for i in self.__canadiate_slots.keys():
                        if re.match('subspace_[GTC]', i) != None and i not in slots1:
                            filled_slots.append(random.choice(self.__canadiate_slots[i]))
                            break
                else:
                    try:
                        filled_slots.append(random.choice(self.__canadiate_slots[slot]))
                    except:
                        pass
            if len(filled_slots)==len(slots1):
                question=template
                for i in range(len(slots)):
                    question=question.replace(slots[i],filled_slots[i],1)
                    fact=self.__fact_generation(simple,slots1,filled_slots)
                question_json={
                    'id':simple['id'],
                    'question': question,
                    'fact': fact
                }
                
        return question_json


    def slotsfilling_from_fact(self,simples,fact):
        fact1=self.__fact_translation(fact)
        sq_fact_json=[]
        for simple in simples:
            if fact1['type']==simple['fact_type']:
                slots=re.findall('<[^<>]*>',simple['modified questions'])
                slots1=re.findall('<([^<>]*)>',simple['modified questions'])
                filled_slots=[]
                for slot in slots1:
                    try:
                        filled_slots.append(fact1[slot])
                    except:
                        pass
                if len(filled_slots) != len(slots1):
                    continue
                question=simple['modified questions']
                for i in range(len(slots)):
                    question=question.replace(slots[i],filled_slots[i],1)
                question_json={
                    'id':simple['id'],
                    'question': question,
                    'fact':fact
                }
                sq_fact_json.append(question_json)
        return sq_fact_json


    def __fact_translation(self,fact):
        pairlist={
            'temporal': 'T',
            'geographical':'G',
            'categorical':'C',
        }
        fact1={}
        for i in fact:
            if i == 'type' and len(fact[i])!=0:
                fact1['type']=fact['type']
            elif i == 'measure' and len(fact[i])!=0:
                measure=random.choice(fact['measure'])
                fact1['measure']=measure['field']
            elif i == 'breakdown' and len(fact[i])!=0:
                breakdown=random.choice(fact['breakdown'])
                fact1['breakdown_%s'%(pairlist[breakdown['type']])]=breakdown['field']
            elif i == 'subspace' and len(fact[i])!=0:
                subspace=random.choice(fact['subspace'])
                fact1['subspace_%s'%(pairlist[subspace['type']])]=subspace['value']
            elif i == 'focus' and len(fact[i])!=0:
                focus=random.choice(fact['focus'])
                fact1['focus']=focus['value']
        return fact1

    def __fact_generation(self,simple,slots1,filled_slots):
        fact={
            'type': simple['fact_type'], 
            'subspace':[
            ],
            'measure':[
            ],
            'breakdown':[
            ],
            'focus':[
            ]
        }
        pairlist={
            'T':'temporal',
            'G':'geographical',
            'C':'categorical'
        }
        for i in range(len(slots1)):
            if slots1[i]=='measure':
                measure={
                    'field':filled_slots[i],
                    'aggregate':'unknown'
                }
                fact['measure'].append(measure)

            elif re.match('subspace_[GTC]', slots1[i]) != None:
                subspace={
                    'field': self.__field_finder(filled_slots[i]),
                    'value': filled_slots[i],
                    'type': pairlist[slots1[i][-1]]
                }
                fact['subspace'].append(subspace)
            elif re.match('breakdown_[GTC]', slots1[i]) != None:
                breakdown={
                    'field': filled_slots[i],
                    'type': pairlist[slots1[i][-1]]
                }
                fact['breakdown'].append(breakdown)
            elif  slots1[i]=='focus':
                focus={
                    'field': self.__field_finder(filled_slots[i]),
                    'value': filled_slots[i]
                }
                fact['focus'].append(focus)
        return fact
    
    def __field_finder(self,value):
        for field in self.__schema:
            if value in field['values']:
                print(field['field'])
                return field['field']


