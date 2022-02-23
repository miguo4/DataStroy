from app.preprocessing.Operator import Operator
import datetime
import numpy
import pandas as pd
import pycountry

class TemGeoNormalizationOpt(Operator):
    #An example operator on data modification
    def __init__(self, data):
        self.data = data

    def start(self):
        self.latlong={}
        pass

    def run(self):
        for field in list(self.data.data['field'].values()):
            df=self.data.data['df'][field['field']]
            if field['type']=='temporal':
                new_df, new_field = _temporalnormalizer(field,df)
                self.data.set_col_label(field['field'],"values",list(map(lambda x: str(x),new_df.fillna('unknown').unique().tolist()))  )
                self.data.set_column(field['field'], new_df)
                self.data.data["field"][field['field']]=new_field
            elif field['type']=='geographical':
                new_df, new_field = _geographicnormalizer(field,df,self.latlong)
                self.data.set_col_label(field['field'],"values",list(map(lambda x: str(x),new_df.fillna('unknown').unique().tolist()))  )
                self.data.set_column(field['field'], new_df)
                self.data.data["field"][field['field']]=new_field
                
    def finish(self):
        pass

def _geographicnormalizer(field,df,latlong):
    #地理信息格式处理
    if field['hierarchy']=='country':
        df=df.apply(_USENCN)
        df=df.apply(_countryabbrevcheck)
        field['values']=list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
    elif field['hierarchy']=='state':
        try:
            df=df.apply(_ChinaENCN)
            field['subtype']='china'
        except:
            try:
                df=df.apply(_usabbrevcheck)
                field['subtype']='usa'
            except:
                pass
        field['values']=list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
    elif field['hierarchy']=='latitude and longtitude':
        if field['subtype']=='latitude':
            latlong['lat']=df
        else:
            latlong['long']=df
        try:
            if len(latlong)==2:
                df='('+latlong['lat'].map(str)+','+ latlong['long'].map(str) + ')'
                field['values']=list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
        except:
            df=df
            field=field
            
    return df,field





def _temporalnormalizer(field,df):
    #更改temporal信息的格式
    if field['hierarchy']=='date':
        df,field= _dateformat(df,field)   
    elif field['hierarchy']=='year':
        df=df.apply(lambda x: _ymdformat(x,year=x))
        field=field
    elif field['hierarchy']=='month':
        try:
            df=pd.to_datetime(df, format='%B').dt.month.astype(str).str.zfill(2)
            # print(df)
        except:
            pass
        # print(field)
        df=df.apply(lambda x: _ymdformat(int(x),month=int(x)))
        field=field
    elif field['hierarchy']=='day':
        df=df.apply(lambda x: _ymdformat(x,day=x))
        field=field
              
    return df, field

def _ymdformat(column,year=1900,month=1,day=1):
    #年月日时间格式处理
    try:
        b=column.strftime("%Y/%m/%d")

    except:        
        b=datetime.date(year, month, day).strftime('%Y/%m/%d')
    return b 


def _dateformat(df,field):
    #date格式处理
    try:
        df=df.apply(timereformat)
    except:
        if type(df[1]) == str:
            if ":" in df[1]:
                try:
                    df=pd.to_datetime(df).dt.strftime('%Y/%m/%d')
                except:
                    try:
                        df=pd.to_datetime(df,format='%m/%d/%Y %H:%M').dt.strftime('%Y/%m/%d')
                    except:
                        field["type"] = "categorical"
                        field["subtype"] = 'unknown'
                        field["values"] = df.fillna('unknown').unique().tolist()
            elif "/" in df[1] or "-" in df[1] :
                try:
                    df=pd.to_datetime(df,format='%Y-%m-%d').dt.strftime('%Y/%m/%d')
                except:
                    try:
                        df=pd.to_datetime(df,format='%m/%d/%Y').dt.strftime('%Y/%m/%d')
                    except:
                        try:
                            df=pd.to_datetime(df,format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
                        except:
                            try:
                                df=pd.to_datetime(df,format='%d-%m-%Y').dt.strftime('%Y/%m/%d')
                            except:
                                try:
                                    df=pd.to_datetime(df,format='%d-%b-%y').dt.strftime('%Y/%m/%d')
                                except:    
                                    field["type"] = "categorical" 
                                    field["subtype"] = 'unknown'
                                    field["values"] = df.fillna('unknown').unique().tolist()
            else:
                field["type"] = "categorical" 
                field["subtype"] = 'unknown'
                field["values"] = df.fillna('unknown').unique().tolist()
        elif type(df[1])==numpy.int64:
            try:
                df=pd.to_datetime(df,format='%Y%m%d').dt.strftime('%Y/%m/%d')
            except:
                field["type"] = "numerical"
                df=df.apply(numericalreformat)
                field["subtype"] = 'unknown'
        elif df.dtype=='datetime64[ns]':
            try:
                df=df.dt.strftime('%Y/%m/%d')
            except:
                pass 
        else:
            try:
                df=df.apply(timereformat)
            except:
                field["type"] = "categorical"   
                field["subtype"] = 'unknown'
                field["values"] = df.fillna('unknown').unique().tolist()
                
    return df, field



def timereformat(column):
    #更改时间格式
    a=pd.to_datetime(datetime.datetime.strptime(column, "%d-%m-%Y").strftime("%Y-%m-%d"),format='%Y-%m-%d').dt.strftime('%Y/%m/%d')
    return a

def _ChinaENCN(column):
    #中国地名汉英翻译
    China1={'新疆': 'Xinjiang', '西藏': 'Xizang', '内蒙古': 'Inner Mongolia', '青海': 'Qinghai', '四川': 'Sichuan', '黑龙江': 'Heilongjiang', '甘肃': 'Gansu', '云南': 'Yunnan', '广西': 'Guangxi', '湖南': 'Hunan', '陕西': 'Shanxi', '广东': 'Guangdong', '吉林': 'Jilin', '河北': 'Hebei', '湖北': 'Hubei', '贵州': 'Guizhou', '山东': 'Shandong', '江西': 'Jiangxi', '河南': 'Henan', '辽宁': 'Liaoning', '山西': 'Shaanxi', '安徽': 'Anhui', '福建': 'Fujian', '浙江': 'Zhejiang', '江苏': 'Jiangsu', '重庆': 'Chongqing', '宁夏': 'Ningxia', '海南': 'Hainan', '台湾': 'Taiwan', '北京': 'Beijing', '天津': 'Tianjin', '上海': 'Shanghai', '香港': 'Hong Kong', '澳门': 'Macau'}
    return [China1[x] for x in China1.keys() if x in column][0]
    # China1={'新疆': 'Xinjiang', '西藏': 'Xizang', '内蒙古': 'Inner Mongolia', '青海': 'Qinghai', '四川': 'Sichuan', '黑龙江': 'Heilongjiang', '甘肃': 'Gansu', '云南': 'Yunnan', '广西': 'Guangxi', '湖南': 'Hunan', '陕西': 'Shanxi', '广东': 'Guangdong', '吉林': 'Jilin', '河北': 'Hebei', '湖北': 'Hubei', '贵州': 'Guizhou', '山东': 'Shandong', '江西': 'Jiangxi', '河南': 'Henan', '辽宁': 'Liaoning', '山西': 'Shaanxi', '安徽': 'Anhui', '福建': 'Fujian', '浙江': 'Zhejiang', '江苏': 'Jiangsu', '重庆': 'Chongqing', '宁夏': 'Ningxia', '海南': 'Hainan', '台湾': 'Taiwan', '北京': 'Beijing', '天津': 'Tianjin', '上海': 'Shanghai', '香港': 'Hong Kong', '澳门': 'Macau'}
    # try: 
    #     return [China1[x] for x in China1.keys() if x in column][0]
    # except:
    #     return [China1[x] for x in China1.values() if x in column][0]



def _USENCN(column):
    #世界国家汉英翻译
    US1={'阿富汗': 'Afghanistan', '安哥拉': 'Angola', '阿尔巴尼亚': 'Albania', '阿拉伯联合酋长国': 'United Arab Emirates', '阿根廷': 'Argentina', '亚美尼亚': 'Armenia', '法属南部领地': 'French Southern and Antarctic Lands', '澳大利亚': 'Australia', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan', '布隆迪': 'Burundi', '比利时': 'Belgium', '贝宁': 'Benin', '布基纳法索': 'Burkina Faso', '孟加拉': 'Bangladesh', '保加利亚': 'Bulgaria', '巴哈马群岛': 'The Bahamas', '波斯尼亚和黑塞哥维那': 'Bosnia and Herzegovina', '白俄罗斯': 'Belarus', '伯利兹': 'Belize', '玻利维亚': 'Bolivia', '巴西': 'Brazil', '文莱': 'Brunei', '不丹': 'Bhutan', '博茨瓦纳': 'Botswana', '中非': 'Central African Republic', '加拿大': 'Canada', '瑞士': 'Swaziland', '智利': 'Chile', '中国': 'China', '象牙海岸': 'Ivory Coast', '喀麦隆': 'Cameroon', '刚果民主共和国': 'Democratic Republic of the Congo', '刚果共和国': 'Republic of the Congo', '哥伦比亚': 'Colombia', '哥斯达黎加': 'Costa Rica', '古巴': 'Cuba', '北塞浦路斯': 'Northern Cyprus', '塞浦路斯': 'Cyprus', '捷克共和国': 'Czech Republic', '德国': 'Germany', '吉布提': 'Djibouti', '丹麦': 'Denmark', '多米尼加共和国': 'Dominican Republic', '阿尔及利亚': 'Algeria', '厄瓜多尔': 'Ecuador', '埃及': 'Egypt', '厄立特里亚': 'Eritrea', '西班牙': 'Spain', '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia', '芬兰': 'Finland', '斐济': 'Fiji', '福克兰群岛': 'Falkland Islands', '法国': 'France', '加蓬': 'Gabon', '英格兰': 'England', '格鲁吉亚': 'Georgia', '加纳': 'Ghana', '几内亚': 'Guinea', '冈比亚': 'Gambia', '几内亚比绍': 'Guinea Bissau', '赤道几内亚': 'Equatorial Guinea', '希腊': 'Greece', '格陵兰岛': 'Greenland', '危地马拉': 'Guatemala', '圭亚那': 'Guyana', '洪都拉斯': 'Honduras', '克罗地亚': 'Croatia', '海地': 'Haiti', '匈牙利': 'Hungary', '印度尼西亚': 'Indonesia', '印度': 'India', '爱尔兰': 'Ireland', '伊朗': 'Iran', '伊拉克': 'Iraq', '冰岛': 'Iceland', '以色列': 'Israel', '意大利': 'Italy', '牙买加': 'Jamaica', '约旦': 'Jordan', '日本': 'Japan', '哈萨克斯坦': 'Kazakhstan', '肯尼亚': 'Kenya', '吉尔吉斯斯坦': 'Kyrgyzstan', '柬埔寨': 'Cambodia', '南韩': 'South Korea', '科索沃': 'Kosovo', '科威特': 'Kuwait', '老挝': 'Laos', '黎巴嫩': 'Lebanon', '利比里亚': 'Liberia', '利比亚': 'Libya', '斯里兰卡': 'Sri Lanka', '莱索托': 'Lesotho', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '拉脱维亚': 'Latvia', '摩洛哥': 'Morocco', '摩尔多瓦': 'Moldova', '马达加斯加': 'Madagascar', '墨西哥': 'Mexico', '马其顿': 'Macedonia', '马里': 'Mali', '缅甸': 'Myanmar', '黑山': 'Montenegro', '蒙古': 'Mongolia', '莫桑比克': 'Mozambique', '毛里塔尼亚': 'Mauritania', '马拉维': 'Malawi', '马来西亚': 'Malaysia', '纳米比亚': 'Namibia', '新喀里多尼亚': 'New Caledonia', '尼日尔': 'Niger', '尼日利亚': 'Nigeria', '尼加拉瓜': 'Nicaragua', '荷兰': 'Netherlands', '挪威': 'Norway', '尼泊尔': 'Nepal', '新西兰': 'New Zealand', '阿曼': 'Oman', '巴基斯坦': 'Pakistan', '巴拿马': 'Panama', '秘鲁': 'Peru', '菲律宾': 'Philippines', '巴布亚新几内亚': 'Papua New Guinea', '波兰': 'Poland', '波多黎各': 'Puerto Rico', '朝鲜': 'North Korea', '葡萄牙': 'Portugal', '巴拉圭;': 'Paraguay', '卡塔尔': 'Qatar', '罗马尼亚': 'Romania', '俄罗斯联邦': 'Russia', '卢旺达': 'Rwanda', '西撒哈拉': 'Western Sahara', '沙特阿拉伯': 'Saudi Arabia', '苏丹': 'Sudan', '南苏丹': 'South Sudan', '塞内加尔': 'Senegal', '所罗门群岛': 'Solomon Islands', '塞拉利昂': 'Sierra Leone', '萨尔瓦多': 'El Salvador', '索马里兰': 'Somaliland', '索马里': 'Somalia', '塞尔维亚共和国': 'Republic of Serbia', '苏里南': 'Suriname', '斯洛伐克': 'Slovakia', '斯洛文尼亚': 'Slovenia', '瑞典': 'Sweden', '叙利亚': 'Syria', '乍得': 'Chad', '多哥': 'Togo', '泰国': 'Thailand', '塔吉克斯坦': 'Tajikistan', '土库曼斯坦': 'Turkmenistan', '东帝汶': 'East Timor', '特立尼达和多巴哥': 'Trinidad and Tobago', '突尼斯': 'Tunisia', '土耳其': 'Turkey', '坦桑尼亚联合共和国': 'United Republic of Tanzania', '乌干达': 'Uganda', '乌克兰': 'Ukraine', '乌拉圭': 'Uruguay', '美国': 'USA', '乌兹别克斯坦': 'Uzbekistan', '委内瑞拉': 'Venezuela', '越南': 'Vietnam', '瓦努阿图': 'Vanuatu', '西岸': 'West Bank', '也门': 'Yemen', '南非': 'South Africa', '赞比亚': 'Zambia', '津巴布韦': 'Zimbabwe'}
    try: 
        a=[US1[x] for x in US1.keys() if x in column][0]
        return a
    except:
        return column

def _usabbrevcheck(column):
    #美国州缩写转全拼
    us_state_abbrev={'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
    abbrev_us_state={'AL': 'Alabama', 'AK': 'Alaska', 'AS': 'American Samoa', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'MP': 'Northern Mariana Islands', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VI': 'Virgin Islands', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
    if column in us_state_abbrev.values():
        return abbrev_us_state[column]
    else:
        raise TimeoutError

def _countryabbrevcheck(column):
    #世界国家缩写转全拼
    list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)]
    list_alpha_3 = [i.alpha_3 for i in list(pycountry.countries)]
    if column in list_alpha_2:
        return pycountry.countries.get(alpha_2=column).name
    elif column in list_alpha_3:
        return pycountry.countries.get(alpha_3=column).name
    else:
        return column
