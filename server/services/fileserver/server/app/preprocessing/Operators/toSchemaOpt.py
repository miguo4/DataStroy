from app.preprocessing.Operator import Operator

class toSchemaOpt(Operator):
    #An example operator on data modification
    def __init__(self, data):
        self.data = data

    def start(self):
        pass

    def run(self):
        field=self.data.data['field']
        statistics=self.data.data['statistics']
        # print(field)
        self.schema = schemagenerator(field,statistics)
    
    def finish(self):
        self.data.set_schema(self.schema)
        # data['statistics']=staticinfo

def schemagenerator(field,statistics):
    schema={
        "statistics":statistics,
        'fields':list(field.values())
    }
    # get the statistics information of a file
    return schema
