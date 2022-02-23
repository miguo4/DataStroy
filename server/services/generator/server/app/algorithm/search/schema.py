# construct a schema graph to guide the search process

class Schema():
    def __init__(self):
        self.fields = []
        self.type2field = {
            "numerical": [],
            "categorical": [],
            "temporal": [],
            "geographical": []
        }
        self.field2type = {}
        self.field2values = {}
        self.field2aggregate = {}


    def add_column(self, field, dtype, values = [], aggregate = []):
        self.fields.append(field.lower())
        self.type2field[dtype].append(field.lower())
        self.field2type[field.lower()] = dtype
        self.field2values[field.lower()] = values
        self.field2aggregate[field.lower()] = aggregate
