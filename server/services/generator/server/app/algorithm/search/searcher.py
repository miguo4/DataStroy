from .q2f import Question2Fact
from .schema import Schema
from ..fact import *
import random
class Searcher:
    def __init__(self, file_schema, file_df):
        self.schema = Schema()
        self.file_df = file_df
        self.file_df.columns = [x.lower() for x in self.file_df.columns]
        for field in file_schema['fields']:
            if field['type'] == 'numerical':
                aggregate = "sum"
                self.schema.add_column(field=field['field'], dtype="numerical", aggregate=aggregate)
            else:
                self.schema.add_column(field=field['field'],
                                       dtype=field['type'],
                                       values=field['values'])
    
        self.q2f = Question2Fact(self.schema,self.file_df)

    def search(self, question):
        facts = self.q2f.generate(question)
        
        return facts
