from app.preprocessing.Operator import Operator

class NormalizationOpt(Operator):
    #仅针对categorical和numerical
    #An example operator on data modification
    def __init__(self, data, colname):
        self.data = data
        self.colname = colname

    def start(self):
        pass
    
    def run(self):
        try:
            df = self.data.data["df"][self.colname]
            column_field=self.data.data['field'][self.colname]
            df = normalizer(column_field, df)
            self.data.set_column(df.name, df)
        except:
            print(self.colname +'_is_deleted')
        

    def finish(self):
        pass

def normalizer(column_field,df):
    #格式标准化处理
    if column_field['type']=='numerical':
        mean_value=column_field['mean']
        df=df.apply(lambda x: _numericalreformat(x,mean_value))
    elif column_field['type']=='categorical':
        df=df.apply(_categoricalreformat)
    return df

def _numericalreformat(column,mean_value):
    #将数值属性的column中掺杂的string变更为field的mean value
    if type(column)==int:
        return column
    elif type(column)==str:
        try:
            return float(column.replace(',', ''))
        except:
            return mean_value
    elif type(column)==float:
        return column
    else:
        return mean_value

def _categoricalreformat(column):
    #保证string返回
    return str(column)




