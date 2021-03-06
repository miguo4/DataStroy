import pandas as pd
import json as js
import time
import pycountry
import datetime
from re import sub 
import numpy
from mxnet import nd
from mxnet.contrib import text
from langdetect import detect
import _pickle as cPickle
import itertools
import re



def is_valid_date(strdate,column):
    try:
        if ":" in strdate:
            time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
        elif "/" in strdate:
            time.strptime(strdate, "%Y/%m/%d")
        else:
            time.strptime(strdate, "%Y-%m-%d")
        return True
    except:
        return False

def engmonth(column):
    try:
        datetime_object = datetime.datetime.strptime(column, "%b")
        month_number = datetime_object.month
        return month_number
    except:
        try:
            datetime_object = datetime.datetime.strptime(column, "%B")
            month_number = datetime_object.month
            return month_number
        except:
            return column

            
def timeformatcheck(df,column,field,statistics):
    if type(df[column][1]) == str:
        if ":" in df[column][1]:
            try:
                df[column]=pd.to_datetime(df[column],format='%Y-%m-%d %H:%M:%S')
                field["subtype"] = 'date'
            except:
                try:
                    df[column]=pd.to_datetime(df[column],format='%m/%d/%Y %H:%M')
                    field["subtype"] = 'date'
                except:
                    field["type"] = "categorical"
                    field["subtype"] = 'unknown'
                    statistics["temporal"] += -1
                    statistics["categorical"] += 1
        elif "/" in df[column][1] or "-" in df[column][1] :
            try:
                df[column]=pd.to_datetime(df[column],format='%Y-%m-%d').dt.strftime('%Y/%m/%d')
                field["subtype"] = 'date'
            except:
                try:
                    df[column]=pd.to_datetime(df[column],format='%m/%d/%Y').dt.strftime('%Y/%m/%d')
                    field["subtype"] = 'date'
                except:
                    try:
                        df[column]=pd.to_datetime(df[column],format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
                        field["subtype"] = 'date'
                    except:
                        try:
                            df[column]=pd.to_datetime(df[column],format='%d-%m-%Y').dt.strftime('%Y/%m/%d')
                            field["subtype"] = 'date'
                        except:
                            field["type"] = "categorical" 
                            field["subtype"] = 'unknown'
                            statistics["temporal"] += -1
                            statistics["categorical"] += 1
        else:
             field["type"] = "categorical" 
             field["subtype"] = 'unknown'
             statistics["temporal"] += -1
             statistics["categorical"] += 1
    elif type(df[column][1])==numpy.int64:
        try:
            df[column]=pd.to_datetime(df[column],format='%Y%m%d').dt.strftime('%Y/%m/%d')
            field["subtype"] = 'date'  
        except:
            field["type"] = "numerical"
            df[column]=df[column].apply(numericalreformat)
            field["subtype"] = 'unknown'
            statistics["temporal"] += -1
            statistics["numerical"] += 1
    else:
        try:
            df[column]=df[column].apply(timereformat)
            field["subtype"] = 'date'
        except:
            field["type"] = "categorical"   
            field["subtype"] = 'unknown'
            statistics["temporal"] += -1
            statistics["categorical"] += 1        


def moneyreformat(column):
    if bool(re.search('[a-z]', column)):
        raise RuntimeError('testError') 
    else:
        c=float(sub(r'[^\d.]', '', column))
        return c




def engcheck(column):
    if bool(re.search('[a-z]', column)):
        return column
    else:
        raise RuntimeError('testError') 


def numericalreformat(column):
    if type(column)==int:
        return column
    elif type(column)==str:
        try:
            return float(column)
        except:
            return 0
    elif type(column)==float:
        return column
    else:
        return 0


def timereformat(column):
    a=pd.to_datetime(datetime.datetime.strptime(column, "%d-%m-%Y").strftime("%Y-%m-%d"),format='%Y-%m-%d').dt.strftime('%Y/%m/%d')
    return a
  

def yearformat(column):
    try:
        b=column.strftime("%Y/%m/%d")
        b=column
    except:        
        b=datetime.date(column, 1, 1).strftime('%Y/%m/%d')
    return b 

def monthformat(column,value):
    try:
        b=column.strftime("%Y/%m/%d")
        b=column
        return b
    except:
        try:
            b=datetime.date(value, column, 1).strftime('%Y/%m/%d')
            return b
        except:
             return column

def dayformat(column,value1,value2):
    try:
        b=column.strftime("%Y/%m/%d")
        b=column
    except:
        b=datetime.date(value1, value2, column).strftime('%Y/%m/%d')
    return b

def ChinaENCN(column):
    China1={'??????': 'Xinjiang', '??????': 'Xizang', '?????????': 'Inner Mongolia', '??????': 'Qinghai', '??????': 'Sichuan', '?????????': 'Heilongjiang', '??????': 'Gansu', '??????': 'Yunnan', '??????': 'Guangxi', '??????': 'Hunan', '??????': 'Shanxi', '??????': 'Guangdong', '??????': 'Jilin', '??????': 'Hebei', '??????': 'Hubei', '??????': 'Guizhou', '??????': 'Shandong', '??????': 'Jiangxi', '??????': 'Henan', '??????': 'Liaoning', '??????': 'Shaanxi', '??????': 'Anhui', '??????': 'Fujian', '??????': 'Zhejiang', '??????': 'Jiangsu', '??????': 'Chongqing', '??????': 'Ningxia', '??????': 'Hainan', '??????': 'Taiwan', '??????': 'Beijing', '??????': 'Tianjin', '??????': 'Shanghai', '??????': 'Hong Kong', '??????': 'Macau'}
    try: 
        a=[China1[x] for x in China1.keys() if x in column][0]
        return a
    except:
        return column

def USENCN(column):
    US1={'?????????': 'Afghanistan', '?????????': 'Angola', '???????????????': 'Albania', '????????????????????????': 'United Arab Emirates', '?????????': 'Argentina', '????????????': 'Armenia', '??????????????????': 'French Southern and Antarctic Lands', '????????????': 'Australia', '?????????': 'Austria', '????????????': 'Azerbaijan', '?????????': 'Burundi', '?????????': 'Belgium', '??????': 'Benin', '???????????????': 'Burkina Faso', '?????????': 'Bangladesh', '????????????': 'Bulgaria', '???????????????': 'The Bahamas', '??????????????????????????????': 'Bosnia and Herzegovina', '????????????': 'Belarus', '?????????': 'Belize', '????????????': 'Bolivia', '??????': 'Brazil', '??????': 'Brunei', '??????': 'Bhutan', '????????????': 'Botswana', '??????': 'Central African Republic', '?????????': 'Canada', '??????': 'Swaziland', '??????': 'Chile', '??????': 'China', '????????????': 'Ivory Coast', '?????????': 'Cameroon', '?????????????????????': 'Democratic Republic of the Congo', '???????????????': 'Republic of the Congo', '????????????': 'Colombia', '???????????????': 'Costa Rica', '??????': 'Cuba', '???????????????': 'Northern Cyprus', '????????????': 'Cyprus', '???????????????': 'Czech Republic', '??????': 'Germany', '?????????': 'Djibouti', '??????': 'Denmark', '?????????????????????': 'Dominican Republic', '???????????????': 'Algeria', '????????????': 'Ecuador', '??????': 'Egypt', '???????????????': 'Eritrea', '?????????': 'Spain', '????????????': 'Estonia', '???????????????': 'Ethiopia', '??????': 'Finland', '??????': 'Fiji', '???????????????': 'Falkland Islands', '??????': 'France', '??????': 'Gabon', '?????????': 'England', '????????????': 'Georgia', '??????': 'Ghana', '?????????': 'Guinea', '?????????': 'Gambia', '???????????????': 'Guinea Bissau', '???????????????': 'Equatorial Guinea', '??????': 'Greece', '????????????': 'Greenland', '????????????': 'Guatemala', '?????????': 'Guyana', '????????????': 'Honduras', '????????????': 'Croatia', '??????': 'Haiti', '?????????': 'Hungary', '???????????????': 'Indonesia', '??????': 'India', '?????????': 'Ireland', '??????': 'Iran', '?????????': 'Iraq', '??????': 'Iceland', '?????????': 'Israel', '?????????': 'Italy', '?????????': 'Jamaica', '??????': 'Jordan', '??????': 'Japan', '???????????????': 'Kazakhstan', '?????????': 'Kenya', '??????????????????': 'Kyrgyzstan', '?????????': 'Cambodia', '??????': 'South Korea', '?????????': 'Kosovo', '?????????': 'Kuwait', '??????': 'Laos', '?????????': 'Lebanon', '????????????': 'Liberia', '?????????': 'Libya', '????????????': 'Sri Lanka', '?????????': 'Lesotho', '?????????': 'Lithuania', '?????????': 'Luxembourg', '????????????': 'Latvia', '?????????': 'Morocco', '????????????': 'Moldova', '???????????????': 'Madagascar', '?????????': 'Mexico', '?????????': 'Macedonia', '??????': 'Mali', '??????': 'Myanmar', '??????': 'Montenegro', '??????': 'Mongolia', '????????????': 'Mozambique', '???????????????': 'Mauritania', '?????????': 'Malawi', '????????????': 'Malaysia', '????????????': 'Namibia', '??????????????????': 'New Caledonia', '?????????': 'Niger', '????????????': 'Nigeria', '????????????': 'Nicaragua', '??????': 'Netherlands', '??????': 'Norway', '?????????': 'Nepal', '?????????': 'New Zealand', '??????': 'Oman', '????????????': 'Pakistan', '?????????': 'Panama', '??????': 'Peru', '?????????': 'Philippines', '?????????????????????': 'Papua New Guinea', '??????': 'Poland', '????????????': 'Puerto Rico', '??????': 'North Korea', '?????????': 'Portugal', '?????????;': 'Paraguay', '?????????': 'Qatar', '????????????': 'Romania', '???????????????': 'Russia', '?????????': 'Rwanda', '????????????': 'Western Sahara', '???????????????': 'Saudi Arabia', '??????': 'Sudan', '?????????': 'South Sudan', '????????????': 'Senegal', '???????????????': 'Solomon Islands', '????????????': 'Sierra Leone', '????????????': 'El Salvador', '????????????': 'Somaliland', '?????????': 'Somalia', '?????????????????????': 'Republic of Serbia', '?????????': 'Suriname', '????????????': 'Slovakia', '???????????????': 'Slovenia', '??????': 'Sweden', '?????????': 'Syria', '??????': 'Chad', '??????': 'Togo', '??????': 'Thailand', '???????????????': 'Tajikistan', '???????????????': 'Turkmenistan', '?????????': 'East Timor', '????????????????????????': 'Trinidad and Tobago', '?????????': 'Tunisia', '?????????': 'Turkey', '???????????????????????????': 'United Republic of Tanzania', '?????????': 'Uganda', '?????????': 'Ukraine', '?????????': 'Uruguay', '??????': 'USA', '??????????????????': 'Uzbekistan', '????????????': 'Venezuela', '??????': 'Vietnam', '????????????': 'Vanuatu', '??????': 'West Bank', '??????': 'Yemen', '??????': 'South Africa', '?????????': 'Zambia', '????????????': 'Zimbabwe'}
    try: 
        a=[US1[x] for x in US1.keys() if x in column][0]
        return a
    except:
        return column


def temporalcheck(column,field,df,hierarchy,statistics,NLPmodel,NLPdataset):
    _list=[i for i in ['date','month','day','utc', 'year','time','??????','??????','???','??????','??????'] if i in column.lower()]
    if 'year' in _list or '???' in _list :
        if df[column].dtype =='int64':
            if any(df[column]<1) or any(df[column]>2070):
                field["type"] = "numerical"
                field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                df[column]=df[column].apply(numericalreformat)
                field["subtype"] = column
                statistics["temporal"] += -1
                statistics["numerical"] += 1
                return True                 
            # elif any(df[column]>0) and any(df[column]<1970):
            #     field["type"] = "categorical"
            #     field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
            #     field["subtype"] = column 
            #     field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)
            #     statistics["temporal"] += -1
            #     statistics["categorical"] += 1
            #     return True 
            else:
                try:
                    field["type"] = "temporal"
                    df[column]=df[column].apply(engmonth)
                    field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                    field["subtype"] = 'year' 
                    field["pictype"] = column
                    hierarchy['year']=column
                    hierarchy['year_value']=df[column]
                    return True            
                except:
                    return False
        else:
            try:
                df[column].apply(yearformat)
                field["type"] = "temporal"
                field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                field["subtype"] = 'year' 
                field["pictype"] = column
                hierarchy['year']=column
                hierarchy['year_value']=df[column]
                return True            
            except:
                field["type"] = "categorical"
                field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
                field["subtype"] = column 
                field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)
                statistics["temporal"] += -1  
                statistics["categorical"] += 1    
                return True
    elif 'month' in _list or '???' in _list:
        if df[column].dtype =='int64':
            if any(df[column]<1) or any(df[column]>12):
                field["type"] = "numerical"
                field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                df[column]=df[column].apply(numericalreformat)
                field["subtype"] = column
                statistics["temporal"] += -1
                statistics["numerical"] += 1
                return True                 
            else:
                try:
                    field["type"] = "temporal"
                    df[column]=df[column].apply(engmonth)
                    field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                    field["subtype"] = 'month' 
                    field["pictype"] = column
                    hierarchy['month']=column
                    hierarchy['month_value']=df[column]
                    return True            
                except:
                    return False
        else:
            try:
                df[column].apply(monthformat) 
                field["type"] = "temporal"
                df[column]=df[column].apply(engmonth)
                field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                field["subtype"] = 'month' 
                field["pictype"] = column
                hierarchy['month']=column
                hierarchy['month_value']=df[column]
                return True            
            except:
                field["type"] = "categorical"
                field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
                field["subtype"] = column 
                field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)
                statistics["temporal"] += -1  
                statistics["categorical"] += 1    
                return True
    elif 'day' in _list or  '???' in _list:
        if df[column].dtype =='int64':
            if any(df[column]<1) or any(df[column]>31):
                field["type"] = "numerical"
                df[column]=df[column].apply(numericalreformat)
                field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                field["subtype"] = column
                statistics["temporal"] += -1
                statistics["numerical"] += 1
                return True                 
            else:
                try:
                    field["type"] = "temporal"
                    field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
                    field["subtype"] = 'day' 
                    field["pictype"] = column
                    hierarchy['day']=column
                    hierarchy['day_value']=df[column]
                    return True            
                except:
                    return False
        elif df[column].dtype =='datetime64[ns]':
            field["type"] = "temporal"
            field["values"] = numpy.array(df[column].fillna('unknown')).tolist()
            field["subtype"] = 'day' 
            field["pictype"] = column
            hierarchy['day']=column
            hierarchy['day_value']=df[column]
            return True 
        else:
            return False

    elif 'date' in _list or 'utc' in _list or 'time' in _list or '??????' in _list or '??????' in _list:  
        if df[column].dtype=="datetime64[ns]":
            field["type"] = "temporal"
            field["subtype"] = _list[0] 
            field["pictype"] = column
            field["values"] = df[column].fillna('unknown').dt.strftime('%Y/%m/%d').unique().tolist()
            return True
        else:
            try:
                field["type"] = "temporal"
                field["subtype"] = _list[0] 
                field["pictype"] = column
                timeformatcheck(df,column,field,statistics)
                field["values"] = df[column].fillna('unknown').unique().tolist()
                return True
            except:
                field["type"] = "categorical"
                field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique()))   
                field["subtype"] = column
                statistics["temporal"] += -1
                statistics["categorical"] += 1
                return True

    elif df[column].dtype == "datetime64[ns]":
        field["type"] = "temporal"
        field["values"] = df[column].fillna('unknown').dt.strftime('%Y/%m/%d').unique().tolist()
        field["subtype"] = 'date'
        field["pictype"] = column
        return True
    elif is_valid_date(column[0],column):
        field["type"] = "temporal"
        field["values"] = df[column].fillna('unknown').unique().tolist()
        field["subtype"] = 'date'
        field["pictype"] = column
        return True
    else:
        return False

def categoricalcheck(column,field,df,NLPmodel,NLPdataset):
    if any(i in column.lower() for i in ['type','category','class','group','??????','??????','???','???','model']):  
        field["type"] = "categorical"
        field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
        field["subtype"] = column 
        field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)     
        return True
    elif df[column].dropna().value_counts().index.isin([0, 1]).all() or len(df[column].dropna().value_counts().index)<=2:
        field["type"] = "categorical"
        field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
        field["subtype"] = 'boolean'
        field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)     
        return True   
    else:
        return False



        
#geographical check
class Countries:
    def __init__(self):
        self.__countries = ['afghanistan', 'aland islands', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas (the)', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia (plurinational state of)', 'bonaire, sint eustatius and saba', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory (the)', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cabo verde', 'cambodia', 'cameroon', 'canada', 'cayman islands (the)', 'central african republic (the)', 'chad', 'chile', 'china', 'christmas island', 'cocos (keeling) islands (the)', 'colombia', 'comoros (the)', 'congo (the democratic republic of the)', 'congo (the)', 'cook islands (the)', 'costa rica', "cote d'ivoire", 'croatia', 'cuba', 'curacao', 'cyprus', 'czechia', 'denmark', 'djibouti', 'dominica', 'dominican republic (the)', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands (the) [malvinas]', 'faroe islands (the)', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories (the)', 'gabon', 'gambia (the)', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdonald islands', 'holy see (the)', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran (islamic republic of)', 'iraq', 'ireland', 'isle of man', 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', "korea (the democratic people's republic of)", 'korea (the republic of)', 'kuwait', 'kyrgyzstan', "lao people's democratic republic (the)", 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia (the former yugoslav republic of)', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands (the)', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia (federated states of)', 'moldova (the republic of)', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands (the)', 'new caledonia', 'new zealand', 'nicaragua', 'niger (the)', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands (the)', 'norway', 'oman', 'pakistan', 'palau', 'palestine, state of', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines (the)', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'reunion', 'romania', 'russian federation (the)', 'rwanda', 'saint barthelemy', 'saint helena, ascension and tristan da cunha', 'saint kitts and nevis', 'saint lucia', 'saint martin (french part)', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten (dutch part)', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and the south sandwich islands', 'south sudan', 'spain', 'sri lanka', 'sudan (the)', 'suriname', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan (province of china)', 'tajikistan', 'tanzania, united republic of', 'thailand', 'timor-leste', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands (the)', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates (the)', 'united kingdom of great britain and northern ireland (the)','USA','US','UK','united states minor outlying islands (the)', 'united states of america (the)', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela (bolivarian republic of)', 'viet nam', 'virgin islands (british)', 'virgin islands (u.s.)', 'wallis and futuna', 'western sahara*', 'yemen', 'zambia', 'zimbabwe',
        "?????????", "???????????????", "????????????", "??????", "????????????????????????", "??????", "??????", "?????????", "?????????", "????????????", "?????????", "????????????", "????????????", "???????????????", "?????????", "????????????", "?????????", "?????????", "????????????", "??????", "?????????", "????????????", "??????", "?????????", "???????????????", "??????", "?????????", "?????????", "?????????", "?????????", "?????????", "??????", "??????", "?????????", "??????", "??????", "?????????", "??????", "????????????", "????????????", "????????????", "?????????", "???????????????", "????????????", "?????????", "??????", "?????????", "????????????", "??????", "???????????????", "??????", "?????????", "?????????", "????????????", "??????", "??????", "??????", "????????????", "???????????????", "??????", "??????", "??????", "??????", "????????????", "??????", "?????????", "???????????????", "??????", "??????", "????????????", "????????????", "?????????", "??????", "????????????", "??????", "??????", "????????????", "?????????", "?????????", "?????????", "?????????", "?????????", "???????????????", "??????", "?????????", "?????????", "????????????????????????", "?????????", "?????????", "?????????", "????????????", "??????", "?????????", "?????????", "????????????", "??????", "????????????", "?????????", "????????????", "??????", "???????????????", "?????????", "????????????", "????????????", "????????????", "???????????????", "??????????????????", "?????????", "??????", "??????", "????????????", "??????", "??????", "????????????", "????????????", "?????????", "?????????", "??????", "?????????", "?????????", "?????????", "????????????", "???????????????", "??????", "??????", "????????????", "??????", "??????", "?????????", "??????", "?????????", "????????????", "????????????", "??????", "????????????", "?????????", "??????", "?????????", "?????????", "??????", "????????????", "?????????", "??????", "?????????", "????????????", "??????", "?????????", "?????????", "?????????", "?????????", "?????????", "??????", "????????????", "?????????", "????????????", "?????????", "????????????", "???????????????", "??????????????????", "?????????", "????????????", "?????????", "??????", "????????????", "???????????????", "????????????", "???????????????", "??????", "??????", "?????????", "????????????", "?????????", "?????????????????????", "???????????????", "?????????", "?????????", "??????????????????????????????", "????????????", "???????????????", "????????????", "????????????", "?????????", "??????", "?????????", "????????????", "????????????", "??????", "?????????", "?????????", "????????????", "????????????", "???????????????", "?????????????????????","?????????", "???????????????",'??????']

    def __call__(self, name, strict=3):
        result = False
        name = name.lower()
        if strict==3:
            for country in self.__countries:
                if country==name:
                    return True
            else:
                return result
        elif strict==2:
            for country in self.__countries:
                if name in country:
                    return True
            else:
                return result
        elif strict==1:
            for country in self.__countries:
                if country.startswith(name):
                    return True
            else:
                return result
        else:
            return result

def latlongcheck(column,a):
    if column.lower().startswith('lat'):
        lat=column
        a.append(lat)        
    elif column.lower().startswith('long'):  
        long=column
        a.append(long)
    


      
def geocheck(column,field,df,a,NLPmodel,NLPdataset,hierarchy):
    China={ '??????':['??????'],'??????':['??????'], '?????????':['?????????'],'?????????':['?????????'],'?????????':['?????????'],'?????????':['?????????'], '?????????':['????????????','?????????','????????????','?????????','?????????','?????????','????????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '??????????????????':['???????????????','?????????','?????????','?????????','?????????','???????????????','???????????????','???????????????','???????????????','?????????','???????????????','????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','????????????????????????'], '????????????':['????????????','???????????????','?????????','?????????','????????????','?????????','?????????','????????????','????????????','????????????','?????????','?????????','??????????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','????????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','?????????','?????????','????????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','????????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','?????????','????????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','????????????','?????????','?????????','?????????','?????????','????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','??????????????????????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','????????????','?????????','?????????','?????????','?????????','?????????','??????????????????????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????????????????':['?????????','?????????','?????????','?????????','?????????','????????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','?????????','?????????'], '?????????':['?????????','?????????','????????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','???????????????????????????','?????????????????????','?????????????????????'], '?????????':['?????????','????????????','?????????','?????????','?????????','?????????','?????????????????????????????????','??????????????????????????????','??????????????????????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????????????????','??????????????????????????????','???????????????????????????','???????????????????????????','?????????????????????','??????????????????????????????','????????????????????????','?????????????????????'], '?????????':['?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????'], '?????????':['?????????','????????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????','?????????????????????','?????????????????????'], '?????????':['?????????','?????????','?????????????????????','?????????????????????','?????????????????????','?????????????????????','?????????????????????','??????????????????????????????'], '?????????????????????':['?????????','????????????','?????????','?????????','?????????'], '???????????????':['?????????','????????????','?????????','?????????','?????????','?????????','????????????'], '????????????????????????':['???????????????','???????????????','????????????','?????????','?????????????????????','???????????????????????????','???????????????????????????','???????????????','?????????????????????????????????','????????????','????????????','????????????????????????','????????????','???????????????'] }
    China1={'??????': 'Xinjiang', '??????': 'Xizang', '?????????': 'Inner Mongolia', '??????': 'Qinghai', '??????': 'Sichuan', '?????????': 'Heilongjiang', '??????': 'Gansu', '??????': 'Yunnan', '??????': 'Guangxi', '??????': 'Hunan', '??????': 'Shanxi', '??????': 'Guangdong', '??????': 'Jilin', '??????': 'Hebei', '??????': 'Hubei', '??????': 'Guizhou', '??????': 'Shandong', '??????': 'Jiangxi', '??????': 'Henan', '??????': 'Liaoning', '??????': 'Shaanxi', '??????': 'Anhui', '??????': 'Fujian', '??????': 'Zhejiang', '??????': 'Jiangsu', '??????': 'Chongqing', '??????': 'Ningxia', '??????': 'Hainan', '??????': 'Taiwan', '??????': 'Beijing', '??????': 'Tianjin', '??????': 'Shanghai', '??????': 'Hong Kong', '??????': 'Macau'}

    US={'California': ['East Rancho Dominguez', 'Moreno Valley', 'North Glendale', 'Santee', 'Silver Lake', 'Ridgecrest', 'El Cajon', 'Santa Maria', 'Elk Grove', 'Garden Grove', 'Upland', 'Porterville', 'Santa Clara', 'Woodland', 'Goleta', 'Agoura', 'Huntington Beach', 'Bellflower', 'Eureka', 'Escondido', 'Santa Clarita', 'Mead Valley', 'Blythe', 'Madera', 'Oxnard Shores', 'Monterey Park', 'San Francisco', 'Avocado Heights', 'Florin', 'Rio Linda', 'Fremont', 'Calexico', 'Barstow', 'South Whittier', 'Castaic', 'San Jose', 'Oroville', 'Rohnert Park', 'Arroyo Grande', 'Morgan Hill', 'Lomita', 'Casa de Oro-Mount Helix', 'Vineyard', 'Downey', 'Fountain Valley', 'Sherman Oaks', 'Aliso Viejo', 'Fallbrook', 'Palm Desert', 'Mountain View', 'South Lake Tahoe', 'Hacienda Heights', 'Sunnyvale', 'Foster City', 'Baldwin Park', 'Chowchilla', 'Ceres', 'San Dimas', 'Northridge', 'National City', 'Tulare', 'Castro Valley', 'Roseville', 'Calabasas', 'Susanville', 'Patterson', 'Antelope', 'Chico', 'Pacific Grove', 'Wasco', 'Glendale', 'Rancho Cordova', 'Hesperia', 'North Highlands', 'Brea', 'Avenal', 'Selma', 'Rancho Mirage', 'San Marcos', 'Stockton', 'Corona', 'Seaside', 'Hemet', 'Chino', 'Paramount', 'Sanger', 'Daly City', 'Culver City', 'Rosemont', 'Banning', 'San Lorenzo', 'Diamond Bar', 'Canoga Park', 'San Pablo', 'Menlo Park', 'San Rafael', 'Clovis', 'Los Banos', 'Coachella', 'Mission Viejo', 'Rancho Palos Verdes', 'Alameda', 'Menifee', 'Tracy', 'Coronado', 'West Covina', 'Dinuba', 'Oxnard', 'West Hills', 'Orinda', 'San Carlos', 'Tustin', 'Claremont', 'Orcutt', 'San Leandro', 'Palmdale', 'Cathedral City', 'Oildale', 'San Bruno', 'Antioch', 'Santa Ana', 'South Yuba City', 'El Segundo', 'Arcata', 'Folsom', 'Placentia', 'Davis', 'Prunedale', 'Manhattan Beach', 'Soledad', 'Truckee', 'Arcadia', 'San Ramon', 'Santa Cruz', 'Reedley', 'South San Francisco', 'Simi Valley', 'Moorpark', 'Palm Springs', 'Ontario', 'Imperial Beach', 'Pico Rivera', 'Cameron Park', 'Lompoc', 'Martinez', 'Suisun', 'Lynwood', 'Redding', 'Glen Avon', 'West Whittier-Los Nietos', 'Paradise', 'Petaluma', 'Brawley', 'Rosemead', 'Millbrae', 'North Hollywood', 'Brentwood', 'Hollister', 'Pleasant Hill', 'East Hemet', 'Dublin', 'Rancho Cucamonga', 'Monrovia', 'Hanford', 'Shafter', 'San Fernando', 'Moraga', 'Cupertino', 'American Canyon', 'Poway', 'Huntington Park', 'Walnut Park', 'Salinas', 'Redwood City', 'Glendora', 'Long Beach', 'Whittier', 'San Pedro', 'Santa Rosa', 'Pinole', 'Pasadena', 'Carmichael', 'Florence-Graham', 'Fullerton', 'Citrus Heights', 'Fair Oaks', 'South Gate', 'Artesia', 'Rubidoux', 'Woodland Hills', 'San Mateo', 'East Palo Alto', 'Orangevale', 'South Pasadena', 'San Juan Capistrano', 'Pleasanton', 'Wildomar', 'Beverly Hills', 'Redondo Beach', 'Agoura Hills', 'Stanton', 'Bay Point', 'Compton', 'Santa Barbara', 'Winter Gardens', 'Carson', 'Ukiah', 'Watsonville', 'Manteca', 'Thousand Oaks', 'Rancho Santa Margarita', 'Palo Alto', 'Clearlake', 'Napa', 'Rocklin', 'Irvine', 'Redlands', 'Twentynine Palms', 'Los Angeles', 'San Luis Obispo', 'El Dorado Hills', 'Pomona', 'Yucca Valley', 'Boyle Heights', 'Chino Hills', 'Costa Mesa', 'Colton', 'Berkeley', 'Barstow Heights', 'Rialto', 'Willowbrook', 'El Monte', 'Santa Paula', 'Adelanto', 'Montebello', 'Dana Point', 'Monterey', 'Chula Vista', 'Pacifica', 'Fillmore', 'Buena Park', 'Yorba Linda', 'Rancho San Diego', 'Burlingame', 'Port Hueneme', 'West Hollywood', 'Arden-Arcade', 'Azusa', 'Fontana', 'Bayside', 'Atascadero', 'Seal Beach', 'East Los Angeles', 'Cypress', 'Ramona', 'Altadena', 'West Sacramento', 'Arvin', 'North Tustin', 'Turlock', 'Modesto', 'Gilroy', 'Norwalk', 'West Puente Valley', 'San Jacinto', 'Torrance', 'Yucaipa', 'Chatsworth', 'Santa Monica', 'Hawthorne', 'Gardena', 'Paso Robles', 'Hermosa Beach', 'Indio', 'Riverbank', 'Sacramento', 'Merced', 'Oakland', 'Mira Loma', 'San Clemente', 'Marina', 'Milpitas', 'El Centro', 'Norco', 'Cerritos', 'Temecula', 'Camarillo', 'Loma Linda', 'Echo Park', 'La Crescenta-Montrose', 'Rowland Heights', 'Los Altos', 'South San Jose Hills', 'Alum Rock', 'San Gabriel', 'Yuba City', 'Murrieta', 'Newport Beach', 'Westmont', 'Covina', 'Perris', 'Foothill Farms', 'Corcoran', 'McKinleyville', 'Bell', 'Duarte', 'Inglewood', 'San Diego', 'Granite Bay', 'Oakley', 'Rosamond', 'South El Monte', 'Desert Hot Springs', 'Bell Gardens', 'Atwater', 'Anaheim', 'Bostonia', 'Hayward', 'Bakersfield', 'Nipomo', 'Temple City', 'Alhambra', 'Santa Fe Springs', 'Benicia', 'Universal City', 'Hercules', 'Saratoga', 'Delano', 'Novato', 'Campbell', 'West Carson', 'San Bernardino', 'Encinitas', 'Los Gatos', 'Galt', 'El Cerrito'], 'Mississippi': ['Clinton', 'Brandon', 'Vicksburg', 'Hattiesburg', 'West Gulfport', 'Olive Branch', 'Laurel', 'Ridgeland', 'Clarksdale', 'Southaven', 'Biloxi', 'Horn Lake', 'Gulfport', 'Pearl', 'Natchez', 'Ocean Springs', 'Starkville', 'Oxford', 'Gautier', 'Tupelo', 'Pascagoula'], 'New York': ['Nanuet', 'Mamaroneck', 'Bensonhurst', 'Bellmore', 'Cohoes', 'Kingston', 'Syracuse', 'Smithtown', 'East New York', 'Borough of Queens', 'Port Washington', 'Gloversville', 'Wantagh', 'Staten Island', 'Levittown', 'Huntington', 'Irondequoit', 'West Babylon', 'East Patchogue', 'New Rochelle', 'Centereach', 'Pearl River', 'Rochester', 'Hauppauge', 'Manhattan', 'Roosevelt', 'Huntington Station', 'Peekskill', 'New York City', 'North Bellmore', 'Valley Stream', 'Westbury', 'Selden', 'Mineola', 'Copiague', 'North Tonawanda', 'Spring Valley', 'Lynbrook', 'Eggertsville', 'North Babylon', 'Holtsville', 'Garden City', 'Jamestown', 'Merrick', 'Mount Vernon', 'Syosset', 'East Setauket', 'Lindenhurst', 'Dix Hills', 'Rotterdam', 'Saratoga Springs', 'Harrison', 'Rockville Centre', 'Central Islip', 'Mastic', 'Newburgh', 'Massapequa Park', 'North Bay Shore', 'White Plains', 'Depew', 'Lockport', 'Glen Cove', 'Beacon', 'Holbrook', 'Brooklyn', 'Cheektowaga', 'Oswego', 'Monsey', 'Sayville', 'Elmont', 'Scarsdale', 'Shirley', 'East Meadow', 'North Amityville', 'Kiryas Joel', 'Plattsburgh', 'Floral Park', 'Greenburgh', 'Binghamton', 'Amsterdam', 'Schenectady', 'Jamaica', 'West Albany', 'North Valley Stream', 'Utica', 'Seaford', 'Setauket-East Setauket', 'Commack', 'East Massapequa', 'Franklin Square', 'North Massapequa', 'Lake Ronkonkoma', 'Coney Island', 'Melville', 'Farmingville', 'Uniondale', 'Eastchester', 'Ithaca', 'Hempstead', 'Bethpage', 'Baldwin', 'Massapequa', 'Bay Shore', 'Freeport', 'Tonawanda', 'Poughkeepsie', 'Lackawanna', 'Woodmere', 'Niagara Falls', 'Albany', 'Islip', 'The Bronx', 'Cortland', 'West Islip', 'Rye', 'West Seneca', 'Long Island City', 'Yonkers', 'Deer Park', 'Elmira', 'Kings Park', 'East Northport', 'Amherst', 'Ronkonkoma', 'Coram', 'Ossining', 'Port Chester', 'New City', 'West Hempstead', 'Hicksville', 'Oceanside'], 'Oklahoma': ['Sand Springs', 'Shawnee', 'Chickasha', 'Mustang', 'Oklahoma City', 'Tahlequah', 'McAlester', 'Lawton', 'Altus', 'Ponca City', 'Claremore', 'Del City', 'Tulsa', 'Bartlesville', 'Muskogee', 'Broken Arrow', 'Ada', 'Jenks', 'Owasso', 'Moore', 'Ardmore', 'Midwest City', 'Stillwater', 'Bixby', 'Enid', 'Sapulpa', 'El Reno', 'Norman', 'Edmond', 'Duncan', 'Yukon', 'Bethany', 'Durant'], 'Maryland': ['Middle River', 'Hagerstown', 'White Oak', 'West Elkridge', 'Eldersburg', 'Rockville', 'Ellicott City', 'Crofton', 'Bethesda', 'Ilchester', 'North Bethesda', 'Calverton', 'Severn', 'Owings Mills', 'Fairland', 'Bel Air South', 'Camp Springs', 'Reisterstown', 'Dundalk', 'Olney', 'Glen Burnie', 'Cockeysville', 'Arbutus', 'Parole', 'Perry Hall', 'Randallstown', 'Wheaton', 'Redland', 'Severna Park', 'Catonsville', 'Essex', 'Elkton', 'Annapolis', 'Oxon Hill', 'Damascus', 'South Bel Air', 'Suitland', 'Langley Park', 'Silver Spring', 'Columbia', 'Lochearn', 'East Riverdale', 'Westminster', 'Elkridge', 'Frederick', 'Bel Air North', 'Potomac', 'Greenbelt', 'Green Haven', 'Chillum', 'Adelphi', 'Salisbury', 'Maryland City', 'Milford Mill', 'South Laurel', 'Baltimore', 'Waldorf', 'Woodlawn', 'North Bel Air', 'Takoma Park', 'Gaithersburg', 'Glassmanor', 'Rosedale', 'Lake Shore', 'Landover', 'Hyattsville', 'Odenton', 'College Park', 'Hillcrest Heights', 'Carney', 'Cumberland', 'North Potomac', 'Montgomery Village', 'Cloverly', 'Edgewood', 'Rossville', 'Pikesville', 'Parkville', 'Fort Washington', 'Beltsville', 'Ballenger Creek', 'Seabrook', 'Hunt Valley', 'Bowie', 'Towson', 'Aspen Hill'], 'Illinois': ['Carbondale', 'Naperville', 'Champaign', 'Rock Island', 'Godfrey', 'Vernon Hills', 'Orland Park', 'Huntley', 'Berwyn', 'Elgin', 'South Elgin', 'Bensenville', 'Crest Hill', 'Evanston', 'Villa Park', 'Urbana', 'Skokie', 'Cary', 'Fairview Heights', 'Lombard', 'Chicago', 'Belvidere', 'Geneva', 'South Holland', 'Goodings Grove', 'La Grange', 'Calumet City', 'Hoffman Estates', 'Palatine', 'Carol Stream', "O'Fallon", 'Pekin', 'Lake Forest', 'Melrose Park', 'Schaumburg', 'East Saint Louis', 'Sterling', 'Park Forest', 'Homer Glen', 'Matteson', 'Blue Island', 'Dolton', 'Shorewood', 'Cahokia', 'Ottawa', 'Des Plaines', 'Algonquin', 'Carpentersville', 'Addison', 'North Aurora', 'Plainfield', 'Lake in the Hills', 'Oak Lawn', 'Franklin Park', 'Morton Grove', 'Machesney Park', 'Libertyville', 'Gurnee', 'Northbrook', 'Glenview', 'Galesburg', 'Edwardsville', 'Evergreen Park', 'Maywood', 'Loves Park', 'Woodridge', 'Highland Park', 'Bolingbrook', 'Park Ridge', 'Tinley Park', 'Kankakee', 'North Peoria', 'Mundelein', 'Lisle', 'Buffalo Grove', 'Roselle', 'Hinsdale', 'Bartlett', 'Sycamore', 'Hanover Park', 'Lemont', 'Rockford', 'Rolling Meadows', 'Mattoon', 'Upper Alton', 'Alton', 'Romeoville', 'North Chicago', 'Belleville', 'Zion', 'Yorkville', 'Elmhurst', 'Prospect Heights', 'Alsip', 'Joliet', 'Arlington Heights', 'Bellwood', 'Glen Ellyn', 'Bridgeview', 'Darien', 'Grayslake', 'West Chicago', 'Round Lake', 'Granite City', 'East Moline', 'East Peoria', 'Bourbonnais', 'Batavia', 'Dixon', 'Bradley', 'Elk Grove Village', 'Crystal Lake', 'Deerfield', 'Oak Forest', 'DeKalb', 'Chicago Heights', 'Wilmette', 'Downers Grove', 'Country Club Hills', 'Elmwood Park', 'Normal', 'Mount Prospect', 'Mokena', 'Woodstock', 'Macomb', 'Round Lake Beach', 'Collinsville', 'Moline', 'Lake Zurich', 'Washington', 'Morton', 'Waukegan', 'Danville', 'Burbank', 'Palos Hills', 'McHenry', 'Cicero', 'New Lenox', 'Streamwood'], 'Idaho': ['Boise', 'Caldwell', 'Lewiston Orchards', 'Kuna', 'Post Falls', 'Rexburg', 'Nampa', 'Eagle', 'Meridian', "Coeur d'Alene", 'Twin Falls', 'Idaho Falls', 'Moscow', 'Pocatello'], 'Nevada': ['Las Vegas', 'Sun Valley', 'Boulder City', 'Spanish Springs', 'Pahrump', 'Fernley', 'Elko', 'Carson City', 'Whitney', 'Sparks', 'North Las Vegas', 'Summerlin South', 'Enterprise', 'Reno', 'Mesquite', 'Sunrise Manor'], 'Colorado': ['Denver', 'Commerce City', 'Southglenn', 'Highlands Ranch', 'Golden', 'Greeley', 'Brighton', 'Parker', 'Loveland', 'Littleton', 'Fountain', 'Windsor', 'Broomfield', 'Cimarron Hills', 'Louisville', 'Longmont', 'Canon City', 'Grand Junction', 'Montrose', 'Castle Rock', 'Wheat Ridge', 'Boulder', 'Pueblo', 'Arvada', 'Erie', 'Sherrelwood', 'Colorado Springs', 'Castlewood', 'Durango', 'Centennial', 'Columbine', 'Security-Widefield', 'Pueblo West', 'Ken Caryl', 'Fort Collins', 'Thornton', 'Northglenn'], 'Florida': ['Venice', 'Bartow', 'Edgewater', 'Allapattah', 'Hollywood', 'Richmond West', 'Pinecrest', 'Homestead', 'Meadow Woods', 'West Little River', 'Country Club', 'Winter Springs', 'Dunedin', 'Palm Valley', 'Naples', 'Casselberry', 'South Bradenton', 'Palm Coast', 'Merritt Island', 'Altamonte Springs', 'DeBary', 'Poinciana', 'Navarre', 'Royal Palm Beach', 'The Crossings', 'Tamarac', 'Fort Lauderdale', 'Carol City', 'Lake Magdalene', 'Titusville', 'Dania Beach', 'Brownsville', 'Largo', 'Jacksonville Beach', 'Ocala', 'Bonita Springs', 'Tampa', 'Bradenton', 'New Smyrna Beach', 'Pompano Beach', 'Miami Gardens', 'Lauderdale Lakes', 'Golden Gate', 'Tallahassee', 'Buenaventura Lakes', 'Brent', 'Crestview', 'Palmetto Bay', 'Coconut Creek', 'Saint Cloud', 'Pinewood', 'Ponte Vedra Beach', 'Pinellas Park', 'Maitland', 'Fort Walton Beach', 'Valrico', 'Cocoa', 'Opa-locka', 'South Miami Heights', 'Ormond Beach', 'Pembroke Pines', 'Lake Worth Corridor', 'Cutler Bay', 'Southchase', 'Keystone', 'Fruit Cove', 'Lauderhill', 'Vero Beach South', 'Ensley', 'Kissimmee', 'Fountainebleau', 'Seminole', "Town 'n' Country", 'Ojus', 'Kendale Lakes', 'Three Lakes', 'Plantation', 'Holiday', 'Wellington', 'Egypt Lake-Leto', 'Miami Beach', 'Temple Terrace', 'Apopka', 'Immokalee', 'Lehigh Acres', 'Oakland Park', 'Sunset', 'Clermont', 'Kendall', 'North Lauderdale', 'East Lake', 'Riverview', 'Rockledge', 'Winter Haven', 'Lakeside', 'Greater Northdale', 'Golden Glades', 'Fort Myers', 'Jupiter', 'Norland', 'Stuart', 'Vero Beach', 'East Pensacola Heights', 'Delray Beach', 'Key West', 'Riviera Beach', 'Spring Hill', 'Boynton Beach', 'Greenacres City', "Land O' Lakes", 'Palm Beach Gardens', 'Hallandale Beach', 'Carrollwood', 'West and East Lealman', 'Winter Garden', 'Eustis', 'Wright', 'Davie', 'Punta Gorda', 'Ferry Pass', 'Lakeland', 'Lake Butler', 'Cantonment', 'Alafaya', 'Deerfield Beach', 'Pace', 'West Palm Beach', 'Iona', 'Country Walk', 'Fort Pierce', 'Citrus Park', 'Bloomingdale', 'Miramar', 'Coral Gables', 'Lake Worth', 'Daytona Beach', 'Flagami', 'Coconut Grove', 'Palm City', 'North Fort Myers', 'North Miami', 'Oviedo', 'Cutler', 'Port Saint Lucie', 'Orlando', 'Carrollwood Village', 'West Pensacola', 'Cutler Ridge', 'Haines City', 'Cape Coral', 'Miami Lakes', 'Bellview', 'Clearwater', 'Plant City', 'Myrtle Grove', 'Wesley Chapel', 'Punta Gorda Isles', 'Boca Del Mar', 'Pine Hills', 'San Carlos Park', 'Bayshore Gardens', 'Westchase', 'Lutz', 'West Melbourne', 'Sebastian', 'East Lake-Orient Park', 'Sunrise', 'Melbourne', 'Aventura', 'Palm Bay', 'Saint Petersburg', 'Glenvar Heights', 'Princeton', 'Sun City Center', 'Ives Estates', 'Pensacola', 'Safety Harbor', 'Tamiami', 'Coral Terrace', 'North Miami Beach', 'Winter Park', 'Coral Springs', 'Sanford', 'Westchester', 'Port Orange', 'Tarpon Springs', 'Hialeah', 'Ruskin', 'Jasmine Estates', 'Florida Ridge', 'Wekiwa Springs', 'Cooper City', 'Miami', 'Deltona', 'Margate', 'Sarasota', 'The Hammocks', 'Belle Glade', 'Panama City', 'Port Charlotte', 'DeLand', 'Bayonet Point', 'Lealman', 'Doral', 'Ocoee', 'North Port', 'Boca Raton', 'Leisure City', 'Hialeah Gardens', 'Palm Harbor', 'The Villages', 'University', 'Sunny Isles Beach', 'Leesburg', 'Weston', 'Estero', 'Lynn Haven'], 'Texas': ['Dallas', 'Brownwood', 'Harlingen', 'Ennis', 'Cloverleaf', 'Farmers Branch', 'Cedar Hill', 'Eagle Pass', 'Plainview', 'Angleton', 'Corpus Christi', 'Bryan', 'Harker Heights', 'Colleyville', 'Amarillo', 'Coppell', 'Channelview', 'Fort Hood', 'Euless', 'Haltom City', 'Edinburg', 'Socorro Mission Number 1 Colonia', 'Beaumont', 'Aldine', 'Balch Springs', 'Flower Mound', 'Alamo', 'Alvin', 'Atascocita', 'Georgetown', 'Denison', 'Del Rio', 'Alice', 'Corinth', 'Groves', 'Garland', 'Big Spring', 'Cedar Park', 'Friendswood', 'Pampa', 'Gainesville', 'West Odessa', 'Socorro', 'Odessa', 'Burleson', 'San Angelo', 'El Paso', 'Copperas Cove', 'Brushy Creek', 'Abilene', 'Bellaire', 'Donna', 'Gatesville', 'Corsicana', 'Houston', 'College Station', 'DeSoto', 'Cinco Ranch', 'Grand Prairie', 'Horizon City', 'Benbrook', 'Galveston', 'Converse', 'Grapevine', 'Cleburne', 'Conroe', 'Hurst', 'Lubbock', 'Cibolo', 'Highland Village', 'Allen', 'Frisco', 'Brenham', 'Fort Worth', 'Humble', 'Baytown', 'Canyon Lake', 'Greenville', 'Fresno', 'Midland', 'Hereford', 'Denton', 'Duncanville'], 'Arkansas': ['Benton', 'Pine Bluff', 'Bentonville', 'Forrest City', 'El Dorado', 'Texarkana', 'Russellville', 'Paragould', 'Bella Vista', 'Jonesboro', 'North Little Rock', 'Conway', 'Little Rock', 'Cabot', 'Searcy', 'Van Buren', 'Jacksonville', 'Rogers', 'Hot Springs National Park', 'Springdale', 'Bryant', 'Maumelle', 'Fort Smith', 'Blytheville', 'Siloam Springs', 'Hot Springs', 'West Memphis'], 'Arizona': ['Lake Havasu City', 'Queen Creek', 'San Luis', 'Apache Junction', 'Surprise', 'Scottsdale', 'Casas Adobes', 'Rio Rico', 'Payson', 'Sun City West', 'Yuma', 'Flowing Wells', 'Fortuna Foothills', 'Chandler', 'Eloy', 'Tucson', 'Casa Grande', 'Tempe', 'Nogales', 'Catalina Foothills', 'Phoenix', 'Douglas', 'Sahuarita', 'Bullhead City', 'Drexel Heights', 'Fountain Hills', 'Anthem', 'Tempe Junction', 'El Mirage', 'Sierra Vista', 'Flagstaff', 'Peoria', 'Maricopa', 'Prescott Valley', 'Mesa', 'Avondale', 'Oro Valley', 'Gilbert', 'Green Valley', 'Goodyear', 'San Tan Valley', 'Kingman', 'Tanque Verde', 'Sun City', 'Prescott', 'Buckeye', 'Marana'], 'Tennessee': ['New South Memphis', 'Tullahoma', 'Lavergne', 'Maryville', 'Lebanon', 'Murfreesboro', 'East Brainerd', 'Nashville', 'Hendersonville', 'Kingsport', 'Chattanooga', 'Mount Juliet', 'Knoxville', 'East Chattanooga', 'Goodlettsville', 'Greeneville', 'Johnson City', 'Collierville', 'Gallatin', 'Germantown', 'Farragut', 'Dyersburg', 'East Ridge', 'Brentwood Estates', 'Cookeville', 'Memphis', 'Oak Ridge'], 'South Carolina': ['North Augusta', 'Goose Creek', 'Greer', 'Summerville', 'Seven Oaks', 'Taylors', 'Socastee', 'North Charleston', 'Myrtle Beach', 'Hilton Head Island', 'Simpsonville', 'Anderson', 'Greenwood', 'Wade Hampton', 'Easley', 'Aiken', 'Hanahan', 'Saint Andrews', 'Mauldin', 'Spartanburg', 'Charleston', 'Rock Hill', 'Sumter'], 'Massachusetts': ['Methuen', 'Natick', 'Shrewsbury', 'Brockton', 'Rockland', 'Yarmouth', 'Westfield', 'South Peabody', 'Everett', 'Taunton', 'Swansea', 'Melrose', 'Sudbury', 'South Hadley', 'Agawam', 'Jamaica Plain', 'Billerica', 'Amesbury', 'Wellesley', 'Worcester', 'Ludlow', 'Acton', 'Haverhill', 'East Longmeadow', 'Dedham', 'Palmer', 'Easthampton', 'Framingham Center', 'Beverly Cove', 'Easton', 'Belmont', 'Fall River', 'Norton', 'Stoneham', 'Longmeadow', 'Lawrence', 'Framingham', 'Chelmsford', 'Lynn', 'Auburn', 'Grafton', 'Springfield', 'New Bedford', 'Wakefield', 'Gloucester', 'Leominster', 'West Springfield', 'Newburyport', 'Chicopee', 'Milton', 'Danvers', 'Winthrop', 'Southbridge', 'Saugus', 'Attleboro', 'Milford', 'Franklin', 'Reading', 'Marblehead', 'Boston', 'South Boston', 'Waltham', 'Amherst Center', 'Holden', 'Westford', 'Ashland', 'North Chicopee', 'Barnstable', 'Northampton', 'Randolph', 'Malden', 'Quincy', 'Lowell', 'Hanover', 'Somerville', 'Braintree', 'Woburn', 'Weymouth', 'Dracut', 'Brookline', 'Chelsea', 'Peabody', 'Stoughton', 'Marlborough', 'Fairhaven', 'Pittsfield', 'Cambridge', 'Watertown', 'Holyoke', 'Needham', 'Tewksbury', 'Abington', 'Beverly'], 'Washington': ['University Place', 'Parkland', 'Aberdeen', 'Lynnwood', 'Monroe', 'Mill Creek', 'Bothell', 'Mukilteo', 'Bremerton', 'Covington', 'Orchards', 'Cottage Lake', 'Shoreline', 'Mercer Island', 'Lake Stevens', 'North Creek', 'Longview', 'Five Corners', 'West Lake Stevens', 'Kennewick', 'Bryn Mawr-Skyway', 'Lacey', 'Ellensburg', 'Spokane Valley', 'Silverdale', 'Salmon Creek', 'City of Sammamish', 'Centralia', 'Edmonds', 'East Hill-Meridian', 'Kent', 'Frederickson', 'Sammamish', 'South Hill', 'Pasco', 'Yakima', 'SeaTac', 'Opportunity', 'Camas', 'Martha Lake', 'Hazel Dell', 'Moses Lake', 'Issaquah', 'Maple Valley', 'Silver Firs', 'Bonney Lake', 'Pullman', 'Tacoma', 'Sunnyside', 'Olympia', 'Walla Walla', 'Burien', 'Lakewood', 'Oak Harbor', 'Puyallup', 'Arlington', 'Renton', 'Redmond', 'Richland', 'Bainbridge Island', 'Battle Ground', 'Port Angeles', 'Tumwater', 'Vancouver', 'Union Hill-Novelty Hill', 'Bellingham', 'Inglewood-Finn Hill', 'Wenatchee', 'Spokane', 'Marysville', 'Tukwila', 'Seattle', 'Spanaway', 'Kenmore', 'Fairwood', 'Graham', 'Mountlake Terrace', 'Anacortes', 'Federal Way', 'West Lake Sammamish', 'Kirkland'], 'Indiana': ['Muncie', 'Carmel', 'Vincennes', 'Mishawaka', 'Clarksville', 'Crown Point', 'Hobart', 'Valparaiso', 'Evansville', 'Fishers', 'LaPorte', 'South Bend', 'Griffith', 'Crawfordsville', 'Shelbyville', 'Brownsburg', 'West Lafayette', 'Schererville', 'East Chicago', 'Munster', 'Jasper', 'New Albany', 'Noblesville', 'Fairfield Heights', 'Kokomo', 'Portage', 'Fort Wayne', 'Broad Ripple', 'Terre Haute', 'Highland', 'Bloomington', 'Seymour', 'Logansport', 'Gary', 'Elkhart', 'Granger', 'Michigan City', 'Hammond', 'Indianapolis', 'Merrillville', 'Goshen', 'Dyer', 'Jeffersonville'], 'Wisconsin': ['North La Crosse', 'Racine', 'Stevens Point', 'De Pere', 'Kenosha', 'Menomonee Falls', 'Menasha', 'Wausau', 'Waukesha', 'New Berlin', 'Mequon', 'Sun Prairie', 'La Crosse', 'Onalaska', 'Fond du Lac', 'West Bend', 'Ashwaubenon', 'Eau Claire', 'Fitchburg', 'Sheboygan', 'Appleton', 'Cudahy', 'Oshkosh', 'Caledonia', 'Janesville', 'Milwaukee', 'Wisconsin Rapids', 'Manitowoc', 'Howard', 'Greenfield', 'Pleasant Prairie', 'Kaukauna', 'Beloit', 'Neenah', 'Marshfield', 'Oconomowoc', 'Muskego', 'Middleton', 'Brookfield', 'South Milwaukee', 'Beaver Dam', 'Menomonie', 'Wauwatosa', 'Oak Creek', 'Superior', 'Green Bay', 'West Allis'], 'Ohio': ['Fairview Park', 'Troy', 'East Cleveland', 'Newark', 'Xenia', 'North Olmsted', 'Huber Heights', 'Bay Village', 'Cincinnati', 'North Royalton', 'Vandalia', 'Avon Center', 'Maple Heights', 'Defiance', 'Grove City', 'Marion', 'Wooster', 'Findlay', 'Willoughby', 'South Euclid', 'Lancaster', 'Gahanna', 'Riverside', 'Rocky River', 'Akron', 'Broadview Heights', 'Green', 'Aurora', 'Eastlake', 'Strongsville', 'Tiffin', 'Perrysburg', 'Avon', 'Sandusky', 'New Philadelphia', 'Beavercreek', 'Norwood', 'Twinsburg', 'Massillon', 'Westlake', 'Pickerington', 'Dayton', 'Sidney', 'Upper Arlington', 'North Ridgeville', 'Hudson', 'Delaware', 'Zanesville', 'Piqua', 'Steubenville', 'Painesville', 'Ashtabula', 'Parma Heights', 'Mentor', 'Westerville', 'Bowling Green', 'Streetsboro', 'Kettering', 'Tallmadge', 'Alliance', 'Warren', 'Hamilton', 'Miamisburg', 'Oregon', 'Fairborn', 'Medina', 'Austintown', 'Parma', 'Wadsworth', 'Mansfield', 'Reynoldsburg', 'Toledo', 'Lima', 'Mayfield Heights', 'Barberton', 'Boardman', 'Trotwood', 'Garfield Heights', 'Whitehall', 'Avon Lake', 'Berea', 'Sylvania', 'Lorain', 'Stow', 'Elyria', 'Mason', 'North Canton', 'Hilliard', 'Solon', 'Cuyahoga Falls', 'Shaker Heights', 'Fairfield', 'Middleburg Heights', 'Youngstown', 'Brook Park', 'Cleveland', 'Euclid', 'Niles', 'Springboro'], 'Missouri': ['Wentzville', 'Fort Leonard Wood', 'Clayton', 'Chesterfield', 'Spanish Lake', 'Warrensburg', 'Webster Groves', 'Ferguson', 'Belton', 'East Independence', 'Cape Girardeau', 'Raymore', 'Maryland Heights', 'Hannibal', 'Affton', 'Ballwin', 'Saint Charles', 'Liberty', 'Sikeston', 'Mehlville', 'Kirksville', 'Jefferson City', 'St. Louis', 'Wildwood', 'Oakville', 'Raytown', 'University City', 'Hazelwood', 'Lemay', 'Ozark', 'Gladstone', 'Grandview', 'Overland', 'Kirkwood', 'Saint Joseph', 'Blue Springs', 'Creve Coeur', 'Concord', 'Arnold', 'Sedalia', "Lee's Summit", 'Nixa', 'Rolla', 'Saint Peters', 'Florissant', 'Joplin', 'Poplar Bluff'], 'New Jersey': ['Livingston', 'Pennsauken', 'West New York', 'Maplewood', 'Montclair', 'Somerset', 'Toms River', 'Colonia', 'Rahway', 'Madison', 'Parsippany', 'Ridgewood', 'Point Pleasant', 'Bridgewater', 'Marlboro', 'Willingboro', 'Cliffside Park', 'Edison', 'Summit', 'Ewing', 'Paterson', 'Jersey City', 'New Milford', 'Nutley', 'Tinton Falls', 'Hoboken', 'Mahwah', 'Piscataway', 'West Orange', 'South Vineland', 'Sicklerville', 'Union City', 'Bloomfield', 'Old Bridge', 'Hopatcong Hills', 'Irvington', 'Iselin', 'Asbury Park', 'Hopatcong', 'Clifton', 'Kearny', 'Woodbridge', 'Warren Township', 'North Bergen', 'West Milford', 'Bridgeton', 'Atlantic City', 'Secaucus', 'Cranford', 'Orange', 'Cherry Hill', 'Teaneck', 'Englewood', 'Bayonne', 'Union', 'Perth Amboy', 'Hackensack', 'Garfield', 'Hillside', 'Lodi', 'New Brunswick', 'Maple Shade', 'Glassboro', 'Fords', 'Pleasantville', 'Carteret', 'Paramus', 'Passaic', 'Fair Lawn', 'South Plainfield', 'East Orange', 'South Orange', 'Linden', 'Palisades Park', 'Lindenwold', 'Wayne', 'Sayreville Junction', 'Camden', 'North Arlington', 'Sayreville', 'Wyckoff', 'Mount Laurel', 'Morristown', 'Rutherford', 'Bergenfield', 'South River', 'Vineland', 'Scotch Plains', 'Millville', 'Avenel', 'Dumont', 'Long Branch', 'Fort Lee', 'South Old Bridge', 'Williamstown', 'Elizabeth', 'Lyndhurst', 'Ocean Acres', 'East Brunswick', 'North Plainfield'], 'Louisiana': ['New Iberia', 'Marrero', 'Prairieville', 'Lafayette', 'Natchitoches', 'Chalmette', 'Gretna', 'Shenandoah', 'Ruston', 'Terrytown', 'Bossier City', 'Opelousas', 'Metairie Terrace', 'Baton Rouge', 'Estelle', 'Central', 'Bayou Cane', 'Metairie', 'Harvey', 'Lake Charles', 'Shreveport', 'New Orleans', 'Kenner', 'Sulphur', 'Alexandria', 'Slidell', 'Houma', 'Laplace'], 'North Carolina': ['Greensboro', 'Cornelius', 'Durham', 'Kinston', 'Kernersville', 'Holly Springs', 'Carrboro', 'Indian Trail', 'Rocky Mount', 'Matthews', 'Garner', 'Mooresville', 'Henderson', 'Raleigh', 'Albemarle', 'Gastonia', 'Wake Forest', 'Goldsboro', 'High Point', 'West Raleigh', 'Fuquay-Varina', 'Fort Bragg', 'Hope Mills', 'Lumberton', 'Thomasville', 'Morrisville', 'Mint Hill', 'New Bern', 'Charlotte', 'Eden', 'Huntersville', 'Clemmons', 'Boone', 'Roanoke Rapids', 'Statesville', 'Asheboro', 'Wilson', 'Morganton', 'Asheville', 'Apex', 'Elizabeth City', 'Lenoir', 'Hickory', 'Kannapolis', 'Havelock', 'Wilmington', 'Laurinburg', 'Chapel Hill', 'Winston-Salem'], 'Kansas': ['Emporia', 'Topeka', 'Lenexa', 'Hays', 'Gardner', 'Junction City', 'Prairie Village', 'Derby', 'Dodge City', 'Great Bend', 'Liberal', 'Hutchinson', 'Olathe', 'Salina', 'Newton', 'Leavenworth', 'Overland Park', 'Kansas City', 'Leawood', 'Wichita', 'Pittsburg'], 'West Virginia': ['Wheeling', 'Weirton', 'Weirton Heights'], 'Connecticut': ['Irving', 'Branford', 'West Torrington', 'West Haven', 'Wethersfield', 'Ansonia', 'City of Milford (balance)', 'Wolcott', 'Willimantic', 'Windham', 'Westport', 'Cheshire', 'Bridgeport', 'Wallingford Center', 'West Hartford', 'Wilton'], 'Alabama': ['Prattville', 'Homewood', 'Center Point', 'Trussville', 'Talladega', 'Florence', 'Montgomery', 'Dothan', 'Dixiana', 'Vestavia Hills', 'Mountain Brook', 'Gadsden', 'Pelham', 'Birmingham', 'Huntsville', 'Bessemer', 'Prichard', 'Tuscaloosa', 'Phenix City', 'Opelika', 'Hueytown', 'Northport', 'Fairhope', 'Tillmans Corner', 'Mobile', 'East Florence', 'Daphne', 'Hoover'], 'Oregon': ['Aloha', 'Oak Grove', 'Lake Oswego', 'Grants Pass', 'Woodburn', 'Four Corners', 'McMinnville', 'Tigard', 'Troutdale', 'Hillsboro', 'Tualatin', 'Newberg', 'Coos Bay', 'Gresham', 'Milwaukie', 'Roseburg', 'Altamont', 'Central Point', 'Hermiston', 'Klamath Falls', 'Sherwood', 'Wilsonville', 'Canby', 'Corvallis', 'Medford', 'Salem', 'Forest Grove', 'Eugene', 'Lents', 'Oregon City', 'Hayesville', 'Portland', 'Pendleton', 'Bend', 'West Linn', 'Keizer'], 'Georgia': ['Dunwoody', 'Carrollton', 'Wilmington Island', 'Americus', 'Augusta', 'Acworth', 'Lithia Springs', 'Milledgeville', 'Columbus', 'Calhoun', 'Newnan', 'St. Marys', 'Hinesville', 'Douglasville', 'Statesboro', 'Roswell', 'Fayetteville', 'McDonough', 'Macon', 'Smyrna', 'Dalton', 'Sandy Springs', 'Snellville', 'Evans', 'Candler-McAfee', 'Marietta', 'Brookhaven', 'Tifton', 'Lawrenceville', 'Alpharetta', 'Atlanta', 'Savannah', 'East Point', 'North Decatur', 'Decatur', 'Athens', 'Pooler', 'Kingsland', 'Sugar Hill', 'Canton', 'Griffin', 'Kennesaw', 'Peachtree City', 'Conyers', 'Belvedere Park', 'Rome', 'Valdosta', 'Stockbridge', 'Warner Robins', 'Tucker', 'Redan', 'Johns Creek', 'Suwanee', 'Forest Park', 'Cartersville', 'Brunswick', 'Mableton', 'Riverdale', 'North Druid Hills'], 'North Dakota': ['Grand Forks', 'Minot', 'Fargo', 'West Fargo', 'Dickinson', 'Bismarck', 'Mandan'], 'Iowa': ['Cedar Falls', 'Marshalltown', 'Council Bluffs', 'Cedar Rapids', 'Waterloo', 'West Des Moines', 'Iowa City', 'Ankeny', 'Urbandale', 'Muscatine', 'Fort Dodge', 'Mason City', 'Ames', 'Clive', 'Coralville', 'Bettendorf', 'Des Moines', 'Dubuque', 'Johnston', 'Sioux City', 'Davenport', 'Ottumwa'], 'Pennsylvania': ['Hazleton', 'Chester', 'State College', 'Upper Saint Clair', 'Murrysville', 'Radnor', 'Limerick', 'West Chester', 'Chambersburg', 'Norristown', 'Scranton', 'New Castle', 'Harrisburg', 'Whitehall Township', 'Cranberry Township', 'McKeesport', 'Johnstown', 'King of Prussia', 'Lansdale', 'Pottstown', 'Altoona', 'Mountain Top', 'Allentown', 'Drexel Hill', 'Philadelphia', 'Phoenixville', 'Williamsport', 'Monroeville', 'Wilkes-Barre', 'Back Mountain', 'Pittsburgh', 'Plum', 'Allison Park', 'Carlisle', 'Willow Grove', 'Bethlehem', 'Penn Hills', 'York', 'Bethel Park', 'Wilkinsburg', 'West Mifflin', 'Mount Lebanon', 'Hermitage'], 'Michigan': ['Burton', 'Ferndale', 'Southfield', 'Eastpointe', 'Lincoln Park', 'Dearborn Heights', 'Detroit', 'Flint', 'Sterling Heights', 'Madison Heights', 'Owosso', 'Jackson', 'Battle Creek', 'West Bloomfield Township', 'Hamtramck', 'Ypsilanti', 'Rochester Hills', 'Redford', 'Livonia', 'Bay City', 'Taylor', 'Hazel Park', 'Grandville', 'Jenison', 'Mount Clemens', 'Saint Clair Shores', 'Westland', 'Novi', 'Waverly', 'Saginaw', 'Farmington Hills', 'Mount Pleasant', 'Okemos', 'Kentwood', 'Holland', 'Holt', 'Shelby', 'Haslett', 'Iron River', 'Muskegon', 'Wyandotte', 'Oak Park', 'East Lansing', 'Wyoming', 'Grand Rapids', 'Adrian', 'Romulus', 'Forest Hills', 'Grosse Pointe Woods', 'Waterford', 'Trenton', 'Pontiac', 'Norton Shores', 'Ann Arbor', 'Allendale', 'Lansing', 'Marquette', 'Southgate', 'Port Huron', 'Kalamazoo', 'Dearborn', 'Allen Park', 'Auburn Hills', 'Walker', 'Royal Oak'], 'Rhode Island': ['West Warwick', 'North Kingstown', 'Warwick', 'Newport', 'Cranston', 'Providence', 'Westerly', 'Bristol', 'North Providence', 'Central Falls', 'Middletown', 'Smithfield', 'Coventry', 'Woonsocket', 'Pawtucket', 'Barrington', 'East Providence'], 'Utah': ['Centerville', 'American Fork', 'Millcreek', 'Magna', 'Herriman', 'Logan', 'Orem', 'Salt Lake City', 'West Valley City', 'Kaysville', 'South Jordan Heights', 'East Millcreek', 'North Salt Lake', 'South Salt Lake', 'Lehi', 'Sandy Hills', 'West Jordan', 'South Ogden', 'Brigham City', 'Midvale', 'Saint George', 'Roy', 'Clearfield', 'Farmington', 'Sandy City', 'Holladay', 'Cottonwood Heights', 'Springville', 'Ogden', 'North Ogden', 'Layton', 'Taylorsville', 'Draper', 'Eagle Mountain', 'Spanish Fork', 'Provo', 'Pleasant Grove', 'South Jordan', 'Cedar City', 'Kearns', 'Riverton', 'Bountiful', 'Tooele'], 'Maine': ['South Portland', 'Bangor', 'South Portland Gardens', 'Lewiston', 'Westbrook', 'Waterville', 'Saco', 'West Scarborough', 'Biddeford'], 'Hawaii': ['Kihei', 'Waipahu', 'Kaneohe', 'Kahului', 'Pearl City', 'Mililani Town', 'Honolulu', 'Wahiawa', 'Wailuku', 'Kailua', 'Schofield Barracks', 'Makakilo City', 'Hilo', 'Ewa Gentry', 'Makakilo'], 'New Mexico': ['South Valley', 'Albuquerque', 'Carlsbad', 'Alamogordo', 'Rio Rancho', 'Santa Fe', 'Las Cruces', 'Gallup', 'Enchanted Hills', 'Hobbs'], 'Kentucky': ['Paducah', 'Erlanger', 'Winchester', 'Hopkinsville', 'Radcliff', 'Newburg', 'Frankfort', 'Lexington-Fayette', 'Richmond', 'Shively', 'Saint Matthews', 'Jeffersontown', 'Valley Station', 'Pleasure Ridge Park', 'Okolona', 'Independence', 'Murray', 'Nicholasville', 'Highview', 'Burlington', 'Meads', 'Lexington', 'Owensboro', 'Ironville', 'Elizabethtown', 'Madisonville', 'Fort Thomas', 'Fern Creek'], 'Minnesota': ['Austin', 'Lino Lakes', 'Moorhead', 'Columbia Heights', 'Blaine', 'Oakdale', 'Chanhassen', 'New Hope', 'Woodbury', 'Edina', 'Chaska', 'Fridley', 'Albert Lea', 'Lakeville', 'Owatonna', 'Red Wing', 'Mankato', 'Minnetonka Mills', 'Ham Lake', 'Shoreview', 'Inver Grove Heights', 'New Brighton', 'Brooklyn Center', 'Prior Lake', 'Saint Paul', 'Champlin', 'Plymouth', 'Sartell', 'Saint Michael', 'Anoka', 'Willmar', 'Coon Rapids', 'Golden Valley', 'Minneapolis', 'Cottage Grove', 'Maple Grove', 'Hopkins', 'Duluth', 'West Saint Paul', 'Crystal', 'South Saint Paul', 'Brooklyn Park', 'Forest Lake', 'Shakopee', 'Hibbing', 'White Bear Lake', 'Faribault', 'Saint Louis Park', 'Richfield', 'Winona', 'Burnsville', 'Buffalo', 'Rosemount', 'Minnetonka', 'Apple Valley', 'Elk River', 'Andover', 'Ramsey', 'West Coon Rapids', 'Northfield', 'Eden Prairie', 'Savage', 'Eagan'], 'Nebraska': ['Norfolk', 'Papillion', 'North Platte', 'Omaha', 'Grand Island', 'Hastings', 'Lincoln', 'Scottsbluff', 'Bellevue', 'Kearney', 'La Vista'], 'Montana': ['Great Falls', 'Kalispell', 'Butte', 'Helena', 'Billings', 'Butte-Silver Bow (Balance)', 'Missoula', 'Bozeman'], 'Alaska': ['Juneau', 'Fairbanks', 'Anchorage', 'Eagle River', 'Badger'], 'South Dakota': ['Rapid City', 'Brookings', 'Mitchell', 'Sioux Falls'], 'Virginia': ['Fort Hunt', 'Oak Hill'], 'New Hampshire': ['Nashua', 'Bedford', 'Laconia', 'Merrimack', 'Manchester', 'Derry', 'Derry Village', 'East Concord', 'Portsmouth', 'Keene'], 'Wyoming': ['Gillette', 'Rock Springs', 'Cheyenne', 'Laramie', 'Casper', 'Sheridan'], 'Vermont': ['South Burlington', 'Colchester', 'Rutland'], 'Delaware': ['Bear', 'Dover'], 'District of Columbia': ['Washington, D.C.']}
        
    _list=[i for i in ['state','country','area','longitude','latitude','region','city','suburb','???','???','???','???','??????','??????','??????','province'] if i in column.lower()]
    if column.strip().lower().startswith('lat') or column.strip().lower().startswith('long') or column.strip().lower().startswith('??????') or column.strip().lower().startswith('??????'):
        field["type"] = "geographical"
        field["values"] = df[column].fillna('unknown').unique().tolist()
        if column.strip().lower().startswith('lat') or column.strip().lower().startswith('??????'):
            a['lat']=column 
            field['subtype']='latitude and longtitude'
            field["pictype"] ='latitude'
        elif column.strip().lower().startswith('long') or column.strip().lower().startswith('??????'):  
            a['long']=column
            field['subtype']='latitude and longtitude'
            field["pictype"] ='longitude'
        if len(a)==2:
            df[column]= '('+df[a['lat']].map(str)+','+ df[a['long']].map(str) + ')'   
            field['subtype']='latitude and longitude'
            field["pictype"] ='latitude'
            a.clear()
        return True 
    elif 'state' in _list or '???' in _list or 'province' in _list:
        field["type"] = "geographical"
        df[column]=df[column].apply(usabbrevcheck)
        try:
            df[column]=df[column].str.strip()
        except:
            print('strip_fail')
        field["values"] = df[column].fillna('unknown').unique().tolist()
        hierarchy['state']=column
        if type(df[column].dropna().any()) is str and (any(df[column][1] in x for x in China.keys()) or any(df[column][1] in x for x in China1.values())):
            field['subtype']='china'
            df[column]=df[column].apply(ChinaENCN)
            field["values"]= df[column].fillna('unknown').unique().tolist()
        elif type(df[column].dropna().any()) is str and any(df[column][1].strip() in x for x in US.keys()):
            field['subtype']='usa'
        elif type(df[column].dropna().any()) is str:
            field['subtype']='world'   
        else:
            field['subtype']='unknown'   
        field["pictype"] =get_similar_glove(_list[0],NLPmodel,NLPdataset)
        return True 
    elif 'area' in _list or 'region' in _list or '??????' in _list:
        field["type"] = "geographical"
        df[column]=df[column].apply(usabbrevcheck)
        try:
            df[column]=df[column].str.strip()
        except:
            print('strip_fail')
        field["values"]= df[column].fillna('unknown').unique().tolist()
        if type(df[column].dropna().any()) is str and any(df[column][1] in x for x in numpy.concatenate(list(China.values()))) :
            field['subtype']='china'
            hierarchy['area']=column
        elif type(df[column].dropna().any()) is str and any(df[column][1] in x for x in numpy.concatenate(list(US.values()))):
            field['subtype']='usa'
            hierarchy['area']=column
        elif type(df[column].dropna().any()) is str:
            field['subtype']='world'   
            hierarchy['area']=column
        else:
            field['subtype']='unknown'   
            hierarchy['area']=column                
        field["pictype"] =get_similar_glove(_list[0],NLPmodel,NLPdataset) 
        return True 
    elif 'city' in _list or '???' in _list:
        field["type"] = "geographical"
        df[column]=df[column].apply(usabbrevcheck)
        try:
            df[column]=df[column].str.strip()
        except:
            print('strip_fail')
        field["values"]= df[column].fillna('unknown').unique().tolist()
        hierarchy['city']=column
        if type(df[column].dropna().any()) is str and any(df[column][1] in x for x in numpy.concatenate(list(China.values()))):
            field['subtype']='china'
        elif type(df[column].dropna().any()) is str and any(df[column][1] in x for x in numpy.concatenate(list(US.values()))):
            field['subtype']='usa'
        elif type(df[column].dropna().any()) is str:
            field['subtype']='world'   
            hierarchy['city']=column
        else:
            field['subtype']='unknown'   
            hierarchy['city']=column                
        field["pictype"] =get_similar_glove(_list[0],NLPmodel,NLPdataset) 
        return True 
    elif 'suburb' in _list or '???' in _list:
        field["type"] = "geographical"
        df[column]=df[column].apply(usabbrevcheck)
        try:
            df[column]=df[column].str.strip()
        except:
            print('strip_fail')
        field["values"]= df[column].fillna('unknown').unique().tolist()
        hierarchy['suburb']=column
        if type(df[column].dropna().any()) is str and any(df[column][1] in x for x in numpy.concatenate(list(China.values()))):
            field['subtype']='china'
        elif type(df[column].dropna().any()) is str and any(df[column][1] in x for x in numpy.concatenate(list(US.values()))):
            field['subtype']='usa'
        elif type(df[column].dropna().any()) is str:
            field['subtype']='world'   
        else:
            field['subtype']='unknown'   
        field["pictype"] =get_similar_glove(_list[0],NLPmodel,NLPdataset) 
        return True 
    elif type(df[column][0])==str:   
        countries = Countries()        
        if countries(df[column][0], strict=3):
            field["type"] = "geographical"
            df[column]=df[column].apply(USENCN)
            field["values"]= df[column].fillna('unknown').unique().tolist()
            field['subtype']='world'
            field["pictype"] =get_similar_glove('country',NLPmodel,NLPdataset)
            hierarchy['country']=column
            return True
        elif df[column][0] in [i.alpha_2 for i in list(pycountry.countries)] or df[column][0] in [i.alpha_3 for i in list(pycountry.countries)]:
            field["type"] = "geographical"
            df[column]=df[column].apply(USENCN)
            field["values"]= df[column].fillna('unknown').unique().tolist()
            field['subtype']='world'
            field["pictype"] =get_similar_glove('country',NLPmodel,NLPdataset)        
            df[column]=df[column].apply(countryabbrevcheck)
            hierarchy['country']=column
            return True
        else:
            return False
    else:       
        return False
    
def usabbrevcheck(column):
    us_state_abbrev={'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
    abbrev_us_state={'AL': 'Alabama', 'AK': 'Alaska', 'AS': 'American Samoa', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'MP': 'Northern Mariana Islands', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VI': 'Virgin Islands', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
    if column in us_state_abbrev.values():
        return abbrev_us_state[column]
    else:
        return column

def countryabbrevcheck(column):
    list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)]
    list_alpha_3 = [i.alpha_3 for i in list(pycountry.countries)]
    if column in list_alpha_2:
        return pycountry.countries.get(alpha_2=column).name
    elif column in list_alpha_3:
        return pycountry.countries.get(alpha_3=column).name
    else:
        return column
   
#ID Check
                        
def idcheck(column,field,df):
    if any(i in column.lower() for i in ['name','rank','??????','??????','??????']) or column.lower()=='id':
        field["type"] = "categorical"
        field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))        
        field["subtype"] = 'id'
        field["pictype"] ='id'
        return True 
    elif df[column].dtype =='int64' and all(df[column][i]<df[column][i+1] for i in range(20)) and all(df[column]<df.shape[0]):
        field["type"] = "categorical"
        field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
        field["subtype"] = 'id' 
        field["pictype"] ='id'  
        return True
    else:
        return False


def knn(W, x, k):
    # ?????????1e-9????????????????????????
    cos = nd.dot(W, x.reshape((-1,))) / (                                    #reshape(-1) ?????????????????????size?????????????????????   nd.dot()??????     
        (nd.sum(W * W, axis=1) + 1e-9).sqrt() * nd.sum(x * x).sqrt())
    topk = nd.topk(cos, k=k, ret_typ='indices').asnumpy().astype('int32')    #nd.asnumpy() mxnet ->numpy
    return topk, [cos[i].asscalar() for i in topk]


def get_similar_glove(column,NLPmodel,NLPdataset):
    embed=NLPmodel
    k=1
    vecs_query=embed.get_vecs_by_tokens(column.lower())
    vecs=embed.get_vecs_by_tokens(NLPdataset)
    topk, cos= knn(vecs,vecs_query,k)
    if numpy.isnan(cos[0]):
        return 'unknow'
    else:
        for i , c in zip(topk[0:],cos[0:]):
            res_data=NLPdataset[i]
        return res_data


def load_schema(df):
    columns = df.columns.values.tolist()
    glove_6b50d = cPickle.load(open("glove_6b50d.pkl","rb"))
    f = open(r"list_fasttext.txt")
    line = f.readline()
    dataset_EN = []
    while line:
        dataset_EN.append(line.split('\n')[0])
        line = f.readline()
    f.close()
    # fasttext_CN = cPickle.load(open("fasttext_CN.pkl","rb"))
    # f = open(r"list_CN.txt",'r', encoding='UTF-8')
    # line = f.readline()
    # dataset_CN = []
    # while line:
    #     # num = list(map(string,line.split()))
    #     dataset_CN.append(line.split('\n')[0])
    #     line = f.readline()
    # f.close()
    statistics = {
        "column": df.shape[1],
        "row": df.shape[0],
        "numerical": 0,
        "categorical": 0,
        "temporal": 0,
        "geographical": 0,
        "column_high_cardinality": 0,
        "column_constant": 0,
    }
    fields = []
    a={}
    hierarchy={}
    for column in columns:
        field = {
            "field": column
        }
        # try:
        #     result=detect(column.lower())   
        #     if result in ['zh-cn' , 'ko']:
        #         NLPmodel=fasttext_CN
        #         NLPdataset=dataset_CN
        #     else:
        #         NLPmodel=glove_6b50d
        #         NLPdataset=dataset_EN
        # except:
        #     NLPmodel=glove_6b50d
        #     NLPdataset=dataset_EN
        NLPmodel=glove_6b50d
        NLPdataset=dataset_EN
        if temporalcheck(column,field,df,hierarchy,statistics,NLPmodel,NLPdataset):
            statistics["temporal"] += 1
        elif geocheck(column,field,df,a,NLPmodel,NLPdataset,hierarchy):
            statistics["geographical"] += 1
        elif idcheck(column,field,df):
            statistics["categorical"] += 1   
        elif categoricalcheck(column,field,df,NLPmodel,NLPdataset):
            statistics["categorical"] += 1
        elif df[column].dtype == "object":
            try:
                df[column]=df[column].apply(moneyreformat)
                field["type"] = "numerical"
                field["values"] = df[column].fillna('unknown').unique().tolist()
                df[column]=df[column].apply(numericalreformat)
                field["subtype"] = column 
                field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)     
                statistics["numerical"] += 1
                field["cardinality"] = df[column].nunique()
            except:
                try:
                    df[column]=df[column].apply(engcheck)
                    field["type"] = "categorical"
                    field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
                    field["subtype"] = column 
                    field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)     
                    statistics["categorical"] += 1
                except:
                    try:
                        float(df[column][1])
                        field["type"] = "numerical"
                        df[column]=df[column].apply(numericalreformat)
                        field["values"] = df[column].fillna('unknown').unique().tolist()
                        field["subtype"] = column 
                        field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)     
                        statistics["numerical"] += 1
                    except:
                        field["type"] = "categorical"
                        field["values"] = list(map(lambda x: str(x),df[column].fillna('unknown').unique().tolist()))   
                        field["subtype"] = column 
                        field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)
                        statistics["categorical"] += 1     
        else:
            field["type"] = "numerical"
            field["values"] = df[column].fillna('unknown').unique().tolist()
            df[column]=df[column].apply(numericalreformat)
            field["subtype"] = column 
            field["pictype"] =get_similar_glove(column,NLPmodel,NLPdataset)     
            statistics["numerical"] += 1
        field["cardinality"] = df[column].nunique()
        if field["type"] == "categorical" and field["cardinality"] == 1:
            statistics["categorical"] -= 1
            statistics["column"] -= 1
            statistics["column_constant"] += 1
            continue

        fields.append(field)
    for i in fields:
        b=i['field']
        for key, value in hierarchy.items():           
            if type(value)== str and b == value :
                if key=='year':
                    i['parent']='not_existed'
                    df[b]=df[b].apply(yearformat)
                    i['values']=df[b].fillna('unknown').unique().tolist()
                elif key=='month':
                    try:
                        i["parent"] = hierarchy['year']
                        merge=itertools.starmap(lambda x,y :monthformat(x, y),zip(df[b],hierarchy['year_value']))
                        a=list(merge)
                        # i['values']=pd.DataFrame(a)
                        # i['values']=a
                        df[b]=pd.DataFrame(a)
                        i['values']=df[b].fillna('unknown').unique().tolist()
                    except:
                        i["parent"]='not_existed'
                        merge=itertools.starmap(lambda x,y :monthformat(x, y),zip(df[b],itertools.repeat(1970)))
                        a=list(merge)
                        # i['values']=pd.DataFrame(a)
                        # i['values']=a
                        df[b]=pd.DataFrame(a)
                        i['values']=df[b].fillna('unknown').unique().tolist()

                elif key=='day':
                    try:
                        i["parent"] = hierarchy['month']
                        try:
                            merge=itertools.starmap(lambda x,y,z:dayformat(x,y,z),zip(df[b],hierarchy['year_value'],hierarchy['month_value']))
                            a=list(merge)
                            # i['values']=pd.DataFrame(a)
                            # i['values']=a
                            df[b]=pd.DataFrame(a)
                            i['values']=df[b].fillna('unknown').unique().tolist()
                        except:
                            try:
                                merge=itertools.starmap(lambda x,y,z:dayformat(x,y,z),zip(df[b],itertools.repeat(1970),hierarchy['month_value']))
                                a=list(merge)
                                # i['values']=pd.DataFrame(a)
                                # i['values']=a
                                df[b]=pd.DataFrame(a)
                                i['values']=df[b].fillna('unknown').unique().tolist()
                            except:
                                print('month_transform_fail')
                                
                    except:
                        i["parent"]='not_existed'
                        merge=itertools.starmap(lambda x,y,z:dayformat(x,y,z),zip(df[b],itertools.repeat(1970),itertools.repeat(1)))
                        a=list(merge)
                        df[b]=pd.DataFrame(a)
                        i['values']=df[b].fillna('unknown').unique().tolist()
                        
                    
                elif key=='country':
                    i['parent']='not_existed'
                elif key=='state':
                    try:
                        i["parent"] = hierarchy['country']
                    except:
                        i["parent"]='not_existed'
                elif key=='city':
                    try:
                        i["parent"] = hierarchy['state']
                    except:
                        i["parent"]='not_existed'
                elif key=='area':
                    try:
                        i["parent"] = hierarchy['state']
                    except:
                        try:
                            i["parent"] = hierarchy['country']
                        except:
                            i["parent"]='not existed'
                elif key=='suburb':
                    try:
                        i["parent"] = hierarchy['city']
                    except:
                        try:
                            i["parent"] = hierarchy['area']
                        except:
                            i["parent"]='not existed'

    return {
        "statistics": statistics,
        "fields": fields
    }
    return df
    


