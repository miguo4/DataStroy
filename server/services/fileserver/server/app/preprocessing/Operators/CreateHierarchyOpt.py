from app.preprocessing.Operator import Operator


class CreateHierarchyOpt(Operator):
    #An example operator on data modification
    def __init__(self, data):
        self.data = data

    def start(self):
        pass
    
    def run(self):
        hierarchy={}
        fields=self.data.data['field']
        field_with_hierarchy = hierarchylabel(fields,hierarchy)
        self.data.set_field(field_with_hierarchy)
    
    def finish(self):
        # data['statistics']=staticinfo
        pass

def hierarchylabel(fields,hierarchy):
    for field in list(fields.values()):
        if field['type']=='temporal':
            hierarchy[field['hierarchy']]=field['field']
        elif field['type']=='geographical':
            hierarchy[field['hierarchy']]=field['field']

    # label hierarcical information in a file
    dict = {
        "year":{
            "child":"month"
        },
        "month":{
            "parent":"year",
            "child":"day"
        },
        "day":{
            "parent":"month"
        },
        "country":{
            "child":"state"
        },
        "state":{
            "parent":"country",
            "child":"city"
        },
        "city":{
            "parent":"state",
            "child":"suburb"
        },
        "suburb":{
            "parent":"city"
        }
    }

    for field in list(fields.values()):
        if field['type']=='temporal' or field['type']=='geographical':
            try:
                x = dict[field['hierarchy']]
            except:
                continue
            try:
                field['child']=hierarchy[x['child']]
            except:
                field['child']='not_existed'

            try:
                field['parent']=hierarchy[x['parent']]
            except:
                field['parent']='not_existed'    

    return fields
