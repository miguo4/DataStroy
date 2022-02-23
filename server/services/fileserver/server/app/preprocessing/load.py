import pandas as pd

def load_df(url):
    # if url == './csvs/CarSales.csv':
    #     return load_carsales()
    # if url == './csvs/nCoV2020.csv':
    #     return load_ncov()
    # if url == './csvs/deadstartup.csv':
    #     return load_startup()
    
    separator = detectDelimiter(url)

    df = None
    for decode in ['utf-8','gbk','gb18030','ansi']:
        try:
            # print('parse csv file: %s, %s'%(decode, separator))    
            df = pd.read_csv(url, sep=separator, encoding=decode, error_bad_lines=False)
            df = df.infer_objects()
            date = [pd.to_datetime(df[x]) if df[x].astype(str).str.match(r'^\d{4}(\-|\/|\.)\d{1,2}\1\d{1,2}$').all() else df[x] for x in df.columns]
            df = pd.concat(date, axis=1, keys=[s.name for s in date])
            break
        except:
            print('csv parsing error : %s, %s'%(decode, separator))
            continue
            
    return df

def detectDelimiter(csvFile):
    with open(csvFile, 'r') as myCsvfile:
        header=myCsvfile.readline()
        if header.find(";")!=-1:
            return ";"
        if header.find(",")!=-1:
            return ","
    #default delimiter (MS Office export)
    return ";"

# def load_carsales():
#     df = pd.read_csv('./csvs/CarSales.csv')
#     df = df.infer_objects()
#     df['Year'] = pd.to_datetime(df['Year'], format ="%Y")
#     return df

# def load_ncov():
#     df = pd.read_csv('./csvs/nCoV2020.csv')
#     df = df.infer_objects()
#     df['Date'] = pd.to_datetime(df['Date'], format ="%Y/%m/%d")
#     return df

# def load_startup():
#     df = pd.read_csv('./csvs/deadstartup.csv')
#     df = df.infer_objects()
#     df['broken year'] = pd.to_datetime(df['broken year'], format ="%Y")
#     return df