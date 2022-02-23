class DataFormat():
    def __init__(self, data):
        #convert dataframe to desired data format
        self.data={"df":data,
                    "field":{},
                    "statistics":{},
                    "schema":{}}

        for col_id in list(data):
            self.data["field"][col_id] = {}

    def __len__(self):
        return len(self.data["df"].columns)

    def merge(self, new_data):
        #merge data
        self.data["df"][new_data.data["df"].columns] = new_data.data["df"]
        #merge attributes
        for colname, label in new_data.data["field"].items():
            self.data["field"][colname]=label
        #merge statistics
        self.data["statistics"] = new_data.data["statistics"]
        #merge schema
        # self.data["schema"] = new_data.data["schema"]
        
    def set_field(self,field):
        self.data["field"] = field
    
    def set_col_label(self, colname, label, attr):
        self.data["field"][colname][label] = attr
 
    def set_statistics(self, statistics):
        self.data["statistics"] = statistics

    def set_schema(self, schema):
        self.data["schema"] = schema

    def set_column(self, colname, new_df):
        self.data["df"][colname] = new_df

    def get_col_attr(self, colname, label):
        return self.data["field"][colname][label]
    
    def remove_col_label(self, colname, label):
        self.data["field"][colname].pop(label, None)
    
    def get_data_by_colnames(self, colnames):
        return self.data["df"][colnames]

    def remove_column (self,colname):
        self.data["df"].pop(colname)

    def remove_entire_label (self,colname):
        self.data["field"].pop(colname)