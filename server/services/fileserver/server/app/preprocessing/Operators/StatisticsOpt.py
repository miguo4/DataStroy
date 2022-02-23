from app.preprocessing.Operator import Operator

class StatisticsOpt(Operator):
    #An example operator on data modification
    def __init__(self, data):
        self.data = data

    def start(self):
        pass
    
    def run(self):
        data=self.data.data
        self.staticinfo = statics(data)
        
    def finish(self):
        self.data.set_statistics(self.staticinfo)

def statics(data):
    # get the statistics information of a file
    
    staticinfo={
        "column": data['df'].shape[1],
        "row": data['df'].shape[0],
        "numerical": 0,
        "categorical": 0,
        "temporal": 0,
        "geographical": 0,
        "ID":0,
        "text":0,
        "column_high_cardinality": 0,
        "column_constant": 0,
    }
    for field in list(data['field'].values()):
        if field['type']=='numerical':
            staticinfo["numerical"]+=1
        elif field['type']=='categorical':
            staticinfo["categorical"]+=1
        elif field['type']=='temporal':
            staticinfo["temporal"]+=1
        elif field['type']=='ID':
            staticinfo["ID"]+=1
        elif field['type']=='text':
            staticinfo["text"]+=1
        else:
            staticinfo["geographical"]+=1
               
    return staticinfo
