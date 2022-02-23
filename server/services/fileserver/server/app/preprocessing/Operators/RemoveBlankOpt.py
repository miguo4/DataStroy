from app.preprocessing.Operator import Operator

class RemoveBlankOpt(Operator):
    #An example operator on data modification
    def __init__(self, data, colname):
        self.data = data
        self.colname = colname

    def start(self):
        pass

    def run(self):
        df = self.data.data["df"][self.colname]
        column_field=self.data.data['field'][self.colname]
        column_type=self.data.get_col_attr(df.name,'type')
        if df.isna().sum()> (df.shape[0]/2):
            self.data.remove_column(df.name)
            self.data.remove_entire_label(df.name)
        elif 'unnamed' in df.name.lower() and column_field['subtype'] != 'id':
            self.data.remove_column(df.name)
            self.data.remove_entire_label(df.name)
        else:
            df = blankremover(column_field,df)
            self.data.set_column(df.name, df)
        # print(self.data.data)
        
    def finish(self):
        pass

def blankremover(column_field,df):
    if column_field['type'] == 'numerical':
        df=df.fillna(column_field['type'])
    elif column_field['type'] == 'temporal':
        df=df.fillna(df[1])
    elif column_field['type'] == 'geographical':
        df=df.fillna(df[1])
    else:
        df=df.fillna('unknown')
    return df
