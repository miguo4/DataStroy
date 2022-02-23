from app.preprocessing.Operator import Operator
import pycountry
import numpy
import datetime
import pandas as pd
import re
from langdetect import detect
import _pickle as cPickle
#label the type of each df.name
class LabelTypeOpt(Operator):
    #An example operator on data labeling
    def __init__(self, data, colname, params={}):
        # print('____' + self.data)
        self.data = data
        self.colname = colname
        self.params = params


    def start(self):
        pass
    
    def run(self):
        self.data.set_col_label(self.colname,"field",self.colname)
        df = self.data.data["df"][self.colname]
        self.df_type = type_checker(df)
    
    def finish(self):
        if self.df_type['type']=='temporal':
            self.data.set_col_label(self.colname,"type",self.df_type['type'])
            self.data.set_col_label(self.colname,"subtype",self.df_type['subtype'])
            self.data.set_col_label(self.colname,"hierarchy",self.df_type['hierarchy'])
            self.data.set_col_label(self.colname,"isUnique",self.df_type['isUnique'])
            self.data.set_col_label(self.colname,"values",self.df_type['values'])

        elif self.df_type['type']=='categorical':
            self.data.set_col_label(self.colname,"type",self.df_type['type'])
            self.data.set_col_label(self.colname,"subtype",self.df_type['subtype'])
            self.data.set_col_label(self.colname,"values",self.df_type['values'])
            self.data.set_col_label(self.colname,"isUnique",self.df_type['isUnique'])

        elif self.df_type['type']=='geographical':
            self.data.set_col_label(self.colname,"type",self.df_type['type'])
            self.data.set_col_label(self.colname,"subtype",self.df_type['subtype'])
            self.data.set_col_label(self.colname,"hierarchy",self.df_type['hierarchy'])
            self.data.set_col_label(self.colname,"values",self.df_type['values'])
            self.data.set_col_label(self.colname,"isUnique",self.df_type['isUnique'])
            self.data.set_col_label(self.colname,"isPostCode",self.df_type['isPostCode'])

        elif self.df_type['type']=='ID':
            self.data.set_col_label(self.colname,"type",self.df_type['type'])
            self.data.set_col_label(self.colname,"subtype",self.df_type['subtype'])
            self.data.set_col_label(self.colname,"values",self.df_type['values'])
        elif self.df_type['type']=='text':
            self.data.set_col_label(self.colname,"type",self.df_type['type'])
        else:
            self.data.set_col_label(self.colname,"type",self.df_type['type'])
            self.data.set_col_label(self.colname,"subtype",self.df_type['subtype'])
            self.data.set_col_label(self.colname,"mean",self.df_type['mean'])
            self.data.set_col_label(self.colname,"median",self.df_type['median'])
            self.data.set_col_label(self.colname,"std",self.df_type['std'])
            self.data.set_col_label(self.colname,"var",self.df_type['var'])
            self.data.set_col_label(self.colname,"aggregate",self.df_type['measure'])

def type_checker(df):
    #先通过column name标记，剩下的再通过df.dtype标记
    df_type={}
    if any(i in df.name.lower() for i in ['description']):
        df_type["type"] = "text"
    elif all(type(i)==str and len(i)>6 for i in df) and any(len(i.split(' '))>4 or len(i.split(','))>4 for i in df):
        df_type["type"] = "text"
    elif any(i in df.name.lower() for i in ['date','month','day','utc', 'year','time','日期','月份','日','年份','时间']):    
        df_type=_temporalcheck(df,df_type)
    elif any(i in df.name.lower() for i in ['type','category','class','group','类型','种类','组','类','model','name','rank','姓名','编号','排名']) or df.name.lower()=='id' or 'ID' in df.name :  
        df_type=_categoricalcheck(df,df_type)
    elif any(i in df.name.lower() for i in ['state','country','area','longitude','latitude','region','city','suburb','州','省','市','区','地区','经度','纬度','province','zipcode','postcode','zip code','post code', 'areacode' , 'area code']):
        df_type=_geographiccheck(df,df_type)
    else:
        df_type= _dtypecheck(df,df_type)
    if df_type['type']=='numerical':
        if df.dtype=='int64':
            if all(df>=0):
                df_type['subtype']='integer+'
            elif all(df<0):
                df_type['subtype']='integer-'
            else:
                df_type['subtype']='integer'
        elif df.dtype=='float64':
            if all(df>=0):
                df_type['subtype']='real+'
            elif all(df<0):
                df_type['subtype']='real-'
            else:
                df_type['subtype']='real'
        else:
            df_type['subtype']='real'
             
    if len(df.dropna().unique()) == df.dropna().size:
        df_type['isUnique'] = True
    else:
        df_type['isUnique'] = False
    return df_type
            
def _temporalcheck(df,df_type):

    if any(i in df.name.lower() for i in ['date','month','day','utc', 'year','time','日期','月份','日','年份','时间']):
        if 'year' in df.name.lower() or '年' in df.name :
            if df.dtype =='int64':
                if any(df<1) or any(df>2050):
                    df_type["type"] = "numerical"
                    df_type["measure"]=['sum','avg']
                    df_type["mean"] = df.mean()
                    df_type["median"] = df.median()
                    df_type["std"] = df.std()
                    df_type["var"] = df.var()
                else:
                    df_type["type"] = "temporal"
                    df_type["subtype"] = 'year' 
                    df_type["hierarchy"] = 'year'
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
            else:
                try:
                    df[0].strftime("%Y/%m/%d")
                    df_type["type"] = "temporal"
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                    df_type["subtype"] = 'year' 
                    df_type["hierarchy"] = 'year' 
                except:
                    df_type["type"] = "categorical"
                    df_type["subtype"] = 'unknown' 
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist())) 
        elif 'month' in df.name.lower() or '月' in df.name.lower():
            if df.dtype =='int64':
                if any(df<1) or any(df>12):
                    df_type["type"] = "numerical"
                    df_type["measure"]=['sum','avg']
                    df_type["mean"] = df.mean()
                    df_type["median"] = df.median()
                    df_type["std"] = df.std()
                    df_type["var"] = df.var()
                else:
                    df_type["type"] = "temporal"
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                    df_type["subtype"] = 'month' 
                    df_type["hierarchy"] = 'month'
            else:
                try:
                    df[0].strftime("%Y/%m/%d")
                    df_type["type"] = "temporal"
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                    df_type["subtype"] = 'month' 
                    df_type["hierarchy"] = 'month' 
                except:
                    try:
                        pd.to_datetime(df, format='%B').dt.month.astype(str).str.zfill(2)
                        df_type["type"] = "temporal"
                        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                        df_type["subtype"] = 'month' 
                        df_type["hierarchy"] = 'month' 
                    except:
                        df_type["type"] = "categorical"
                        df_type["subtype"] = 'unknown'
                        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))  
        elif 'day' in df.name.lower() or  '日' in df.name.lower():
            if df.dtype =='int64':
                if any(df<1) and any(df>31):
                    df_type["type"] = "numerical"
                    df_type["measure"]=['sum','avg']
                    df_type["mean"] = df.mean()
                    df_type["median"] = df.median()
                    df_type["std"] = df.std()
                    df_type["var"] = df.var()
                else:
                    df_type["type"] = "temporal"
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                    df_type["subtype"] = 'day' 
                    df_type["hierarchy"] = 'day'
            elif df.dtype =='datetime64[ns]':
                df_type["type"] = "temporal"
                df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                df_type["subtype"] = 'day' 
                df_type["hierarchy"] = 'day'
            else:
                try:
                    df[0].strftime("%Y/%m/%d")
                    df_type["type"] = "temporal"
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                    df_type["subtype"] = 'day' 
                    df_type["hierarchy"] = 'day' 
                except:
                    df_type["type"] = "categorical"
                    df_type["subtype"] = 'unknown'
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))  
        else:
            if df.dtype=="datetime64[ns]":
                df_type["type"] = "temporal"
                df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                df_type["subtype"] = 'date' 
                df_type["hierarchy"] = 'date'
            else:
                try:
                    df_type["type"] = "temporal"
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
                    df_type["subtype"] ='date'
                    df_type["hierarchy"]='date'
                    df_type=_timeformatcheck(df,df_type)
                except:
                    df_type["type"] = "categorical"
                    df_type["subtype"] = 'unknown'
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
    return df_type



def _timeformatcheck(df,df_type):
    #地理信息check，先通过column name标记，剩下的再通过df.dtype标记
    if type(df[1]) == str:
        if ":" in df[1]:
            try:
                df=pd.to_datetime(df,format='%Y/%m/%d %H:%M:%S')
                df_type["subtype"] = 'date'
            except:
                try:
                    df=pd.to_datetime(df,format='%m/%d/%Y %H:%M')
                    df_type["subtype"] = 'date'
                except:
                    df_type["type"] = "categorical"
                    df_type["subtype"] = 'unknown'
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
        elif "/" in df[1] or "-" in df[1] :
            try:
                df=pd.to_datetime(df,format='%Y-%m-%d').dt.strftime('%Y/%m/%d')
                df_type["subtype"] = 'date'
                
            except:
                try:
                    df=pd.to_datetime(df,format='%m/%d/%Y').dt.strftime('%Y/%m/%d')
                    df_type["subtype"] = 'date'
                    
                except:
                    try:
                        df=pd.to_datetime(df,format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
                        df_type["subtype"] = 'date'                        
                    except:
                        try:
                            df=pd.to_datetime(df,format='%d-%m-%Y').dt.strftime('%Y/%m/%d')
                            df_type["subtype"] = 'date'
                            
                        except:
                            try:
                                df=df.dt.strftime('%Y/%m/%d')
                                df_type["subtype"] = 'date'                                
                            except:
                                try:
                                    df=pd.to_datetime(df,format='%d-%b-%y').dt.strftime('%Y/%m/%d')
                                    df_type["subtype"] = 'date' 
                                except:
                                    df_type["type"] = "categorical" 
                                    df_type["subtype"] = 'unknown'
                                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
        else:
            df_type["type"] = "categorical" 
            df_type["subtype"] = 'unknown'
            df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist())) 
    elif type(df[1])==numpy.int64:
        try:
            df=pd.to_datetime(df,format='%Y%m%d').dt.strftime('%Y/%m/%d')
            df_type["subtype"] = 'date'  
        except:
            df_type["type"] = "numerical"
            df_type["measure"]=['sum','avg']
            df_type["mean"] = df.mean()
            df_type["median"] = df.median()
            df_type["std"] = df.std()
            df_type["var"] = df.var()

    else:
        try:
            pd.to_datetime(datetime.datetime.strptime(df[1], "%d-%m-%Y").strftime("%Y-%m-%d"),format='%Y-%m-%d').dt.strftime('%Y/%m/%d')
            df_type["subtype"] = 'date'
        except:
            df_type["type"] = "categorical"   
            df_type["subtype"] = 'unknown'
            df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))

    return df_type
        
def _categoricalcheck(df,df_type):
    if any(i in df.name.lower() for i in ['type','category','class','group','类型','种类','组','类','model','unnamed']):  
        df_type["type"] = "categorical"
        df_type["subtype"] = df.name 
        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))  
    else:
        # df_type["type"] = "ID"
        df_type["type"] = "categorical"
        df_type["subtype"] = 'id'
        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))

    return  df_type  

def _geographiccheck(df,df_type):
    _China={ '香港':['香港'],'澳门':['澳门'], '北京市':['北京市'],'天津市':['天津市'],'上海市':['上海市'],'重庆市':['重庆市'], '河北省':['石家庄市','唐山市','秦皇岛市','邯郸市','邢台市','保定市','张家口市','承德市','沧州市','廊坊市','衡水市'], '山西省':['太原市','大同市','阳泉市','长治市','晋城市','朔州市','晋中市','运城市','忻州市','临汾市','吕梁市'], '内蒙古自治区':['呼和浩特市','包头市','乌海市','赤峰市','通辽市','鄂尔多斯市','呼伦贝尔市','巴彦淖尔市','乌兰察布市','兴安盟','锡林郭勒盟','阿拉善盟'], '辽宁省':['沈阳市','大连市','鞍山市','抚顺市','本溪市','丹东市','锦州市','营口市','阜新市','辽阳市','盘锦市','铁岭市','朝阳市','葫芦岛市'], '吉林省':['长春市','吉林市','四平市','辽源市','通化市','白山市','松原市','白城市','延边朝鲜族自治州'], '黑龙江省':['哈尔滨市','齐齐哈尔市','鸡西市','鹤岗市','双鸭山市','大庆市','伊春市','佳木斯市','七台河市','牡丹江市','黑河市','绥化市','大兴安岭地区'], '江苏省':['南京市','无锡市','徐州市','常州市','苏州市','南通市','连云港市','淮安市','盐城市','扬州市','镇江市','泰州市','宿迁市'], '浙江省':['杭州市','宁波市','温州市','嘉兴市','湖州市','绍兴市','金华市','衢州市','舟山市','台州市','丽水市'], '安徽省':['合肥市','芜湖市','蚌埠市','淮南市','马鞍山市','淮北市','铜陵市','安庆市','黄山市','滁州市','阜阳市','宿州市','六安市','亳州市','池州市','宣城市'], '福建省':['福州市','厦门市','莆田市','三明市','泉州市','漳州市','南平市','龙岩市','宁德市'], '江西省':['南昌市','景德镇市','萍乡市','九江市','新余市','鹰潭市','赣州市','吉安市','宜春市','抚州市','上饶市'], '山东省':['济南市','青岛市','淄博市','枣庄市','东营市','烟台市','潍坊市','济宁市','泰安市','威海市','日照市','莱芜市','临沂市','德州市','聊城市','滨州市','菏泽市'], '河南省':['郑州市','开封市','洛阳市','平顶山市','安阳市','鹤壁市','新乡市','焦作市','濮阳市','许昌市','漯河市','三门峡市','南阳市','商丘市','信阳市','周口市','驻马店市'], '湖北省':['武汉市','黄石市','十堰市','宜昌市','襄阳市','鄂州市','荆门市','孝感市','荆州市','黄冈市','咸宁市','随州市','恩施土家族苗族自治州'], '湖南省':['长沙市','株洲市','湘潭市','衡阳市','邵阳市','岳阳市','常德市','张家界市','益阳市','郴州市','永州市','怀化市','娄底市','湘西土家族苗族自治州'], '广东省':['广州市','韶关市','深圳市','珠海市','汕头市','佛山市','江门市','湛江市','茂名市','肇庆市','惠州市','梅州市','汕尾市','河源市','阳江市','清远市','东莞市','中山市','潮州市','揭阳市','云浮市'], '广西壮族自治区':['南宁市','柳州市','桂林市','梧州市','北海市','防城港市','钦州市','贵港市','玉林市','百色市','贺州市','河池市','来宾市','崇左市'], '海南省':['海口市','三亚市','三沙市','儋州市'], '四川省':['成都市','自贡市','攀枝花市','泸州市','德阳市','绵阳市','广元市','遂宁市','内江市','乐山市','南充市','眉山市','宜宾市','广安市','达州市','雅安市','巴中市','资阳市','阿坝藏族羌族自治州','甘孜藏族自治州','凉山彝族自治州'], '贵州省':['贵阳市','六盘水市','遵义市','安顺市','毕节市','铜仁市','黔西南布依族苗族自治州','黔东南苗族侗族自治州','黔南布依族苗族自治州'], '云南省':['昆明市','曲靖市','玉溪市','保山市','昭通市','丽江市','普洱市','临沧市','楚雄彝族自治州','红河哈尼族彝族自治州','文山壮族苗族自治州','西双版纳傣族自治州','大理白族自治州','德宏傣族景颇族自治州','怒江傈僳族自治州','迪庆藏族自治州'], '陕西省':['西安市','铜川市','宝鸡市','咸阳市','渭南市','延安市','汉中市','榆林市','安康市','商洛市'], '甘肃省':['兰州市','嘉峪关市','金昌市','白银市','天水市','武威市','张掖市','平凉市','酒泉市','庆阳市','定西市','陇南市','临夏回族自治州','甘南藏族自治州'], '青海省':['西宁市','海东市','海北藏族自治州','黄南藏族自治州','海南藏族自治州','果洛藏族自治州','玉树藏族自治州','海西蒙古族藏族自治州'], '宁夏回族自治区':['银川市','石嘴山市','吴忠市','固原市','中卫市'], '西藏自治区':['拉萨市','日喀则市','昌都市','林芝市','山南市','那曲市','阿里地区'], '新疆维吾尔自治区':['乌鲁木齐市','克拉玛依市','吐鲁番市','哈密市','昌吉回族自治州','博尔塔拉蒙古自治州','巴音郭楞蒙古自治州','阿克苏地区','克孜勒苏柯尔克孜自治州','喀什地区','和田地区','伊犁哈萨克自治州','塔城地区','阿勒泰地区'] }
    _China1={'新疆': 'Xinjiang', '西藏': 'Xizang', '内蒙古': 'Inner Mongolia', '青海': 'Qinghai', '四川': 'Sichuan', '黑龙江': 'Heilongjiang', '甘肃': 'Gansu', '云南': 'Yunnan', '广西': 'Guangxi', '湖南': 'Hunan', '陕西': 'Shanxi', '广东': 'Guangdong', '吉林': 'Jilin', '河北': 'Hebei', '湖北': 'Hubei', '贵州': 'Guizhou', '山东': 'Shandong', '江西': 'Jiangxi', '河南': 'Henan', '辽宁': 'Liaoning', '山西': 'Shaanxi', '安徽': 'Anhui', '福建': 'Fujian', '浙江': 'Zhejiang', '江苏': 'Jiangsu', '重庆': 'Chongqing', '宁夏': 'Ningxia', '海南': 'Hainan', '台湾': 'Taiwan', '北京': 'Beijing', '天津': 'Tianjin', '上海': 'Shanghai', '香港': 'Hong Kong', '澳门': 'Macau'}
    _US={'California': ['East Rancho Dominguez', 'Moreno Valley', 'North Glendale', 'Santee', 'Silver Lake', 'Ridgecrest', 'El Cajon', 'Santa Maria', 'Elk Grove', 'Garden Grove', 'Upland', 'Porterville', 'Santa Clara', 'Woodland', 'Goleta', 'Agoura', 'Huntington Beach', 'Bellflower', 'Eureka', 'Escondido', 'Santa Clarita', 'Mead Valley', 'Blythe', 'Madera', 'Oxnard Shores', 'Monterey Park', 'San Francisco', 'Avocado Heights', 'Florin', 'Rio Linda', 'Fremont', 'Calexico', 'Barstow', 'South Whittier', 'Castaic', 'San Jose', 'Oroville', 'Rohnert Park', 'Arroyo Grande', 'Morgan Hill', 'Lomita', 'Casa de Oro-Mount Helix', 'Vineyard', 'Downey', 'Fountain Valley', 'Sherman Oaks', 'Aliso Viejo', 'Fallbrook', 'Palm Desert', 'Mountain View', 'South Lake Tahoe', 'Hacienda Heights', 'Sunnyvale', 'Foster City', 'Baldwin Park', 'Chowchilla', 'Ceres', 'San Dimas', 'Northridge', 'National City', 'Tulare', 'Castro Valley', 'Roseville', 'Calabasas', 'Susanville', 'Patterson', 'Antelope', 'Chico', 'Pacific Grove', 'Wasco', 'Glendale', 'Rancho Cordova', 'Hesperia', 'North Highlands', 'Brea', 'Avenal', 'Selma', 'Rancho Mirage', 'San Marcos', 'Stockton', 'Corona', 'Seaside', 'Hemet', 'Chino', 'Paramount', 'Sanger', 'Daly City', 'Culver City', 'Rosemont', 'Banning', 'San Lorenzo', 'Diamond Bar', 'Canoga Park', 'San Pablo', 'Menlo Park', 'San Rafael', 'Clovis', 'Los Banos', 'Coachella', 'Mission Viejo', 'Rancho Palos Verdes', 'Alameda', 'Menifee', 'Tracy', 'Coronado', 'West Covina', 'Dinuba', 'Oxnard', 'West Hills', 'Orinda', 'San Carlos', 'Tustin', 'Claremont', 'Orcutt', 'San Leandro', 'Palmdale', 'Cathedral City', 'Oildale', 'San Bruno', 'Antioch', 'Santa Ana', 'South Yuba City', 'El Segundo', 'Arcata', 'Folsom', 'Placentia', 'Davis', 'Prunedale', 'Manhattan Beach', 'Soledad', 'Truckee', 'Arcadia', 'San Ramon', 'Santa Cruz', 'Reedley', 'South San Francisco', 'Simi Valley', 'Moorpark', 'Palm Springs', 'Ontario', 'Imperial Beach', 'Pico Rivera', 'Cameron Park', 'Lompoc', 'Martinez', 'Suisun', 'Lynwood', 'Redding', 'Glen Avon', 'West Whittier-Los Nietos', 'Paradise', 'Petaluma', 'Brawley', 'Rosemead', 'Millbrae', 'North Hollywood', 'Brentwood', 'Hollister', 'Pleasant Hill', 'East Hemet', 'Dublin', 'Rancho Cucamonga', 'Monrovia', 'Hanford', 'Shafter', 'San Fernando', 'Moraga', 'Cupertino', 'American Canyon', 'Poway', 'Huntington Park', 'Walnut Park', 'Salinas', 'Redwood City', 'Glendora', 'Long Beach', 'Whittier', 'San Pedro', 'Santa Rosa', 'Pinole', 'Pasadena', 'Carmichael', 'Florence-Graham', 'Fullerton', 'Citrus Heights', 'Fair Oaks', 'South Gate', 'Artesia', 'Rubidoux', 'Woodland Hills', 'San Mateo', 'East Palo Alto', 'Orangevale', 'South Pasadena', 'San Juan Capistrano', 'Pleasanton', 'Wildomar', 'Beverly Hills', 'Redondo Beach', 'Agoura Hills', 'Stanton', 'Bay Point', 'Compton', 'Santa Barbara', 'Winter Gardens', 'Carson', 'Ukiah', 'Watsonville', 'Manteca', 'Thousand Oaks', 'Rancho Santa Margarita', 'Palo Alto', 'Clearlake', 'Napa', 'Rocklin', 'Irvine', 'Redlands', 'Twentynine Palms', 'Los Angeles', 'San Luis Obispo', 'El Dorado Hills', 'Pomona', 'Yucca Valley', 'Boyle Heights', 'Chino Hills', 'Costa Mesa', 'Colton', 'Berkeley', 'Barstow Heights', 'Rialto', 'Willowbrook', 'El Monte', 'Santa Paula', 'Adelanto', 'Montebello', 'Dana Point', 'Monterey', 'Chula Vista', 'Pacifica', 'Fillmore', 'Buena Park', 'Yorba Linda', 'Rancho San Diego', 'Burlingame', 'Port Hueneme', 'West Hollywood', 'Arden-Arcade', 'Azusa', 'Fontana', 'Bayside', 'Atascadero', 'Seal Beach', 'East Los Angeles', 'Cypress', 'Ramona', 'Altadena', 'West Sacramento', 'Arvin', 'North Tustin', 'Turlock', 'Modesto', 'Gilroy', 'Norwalk', 'West Puente Valley', 'San Jacinto', 'Torrance', 'Yucaipa', 'Chatsworth', 'Santa Monica', 'Hawthorne', 'Gardena', 'Paso Robles', 'Hermosa Beach', 'Indio', 'Riverbank', 'Sacramento', 'Merced', 'Oakland', 'Mira Loma', 'San Clemente', 'Marina', 'Milpitas', 'El Centro', 'Norco', 'Cerritos', 'Temecula', 'Camarillo', 'Loma Linda', 'Echo Park', 'La Crescenta-Montrose', 'Rowland Heights', 'Los Altos', 'South San Jose Hills', 'Alum Rock', 'San Gabriel', 'Yuba City', 'Murrieta', 'Newport Beach', 'Westmont', 'Covina', 'Perris', 'Foothill Farms', 'Corcoran', 'McKinleyville', 'Bell', 'Duarte', 'Inglewood', 'San Diego', 'Granite Bay', 'Oakley', 'Rosamond', 'South El Monte', 'Desert Hot Springs', 'Bell Gardens', 'Atwater', 'Anaheim', 'Bostonia', 'Hayward', 'Bakersfield', 'Nipomo', 'Temple City', 'Alhambra', 'Santa Fe Springs', 'Benicia', 'Universal City', 'Hercules', 'Saratoga', 'Delano', 'Novato', 'Campbell', 'West Carson', 'San Bernardino', 'Encinitas', 'Los Gatos', 'Galt', 'El Cerrito'], 'Mississippi': ['Clinton', 'Brandon', 'Vicksburg', 'Hattiesburg', 'West Gulfport', 'Olive Branch', 'Laurel', 'Ridgeland', 'Clarksdale', 'Southaven', 'Biloxi', 'Horn Lake', 'Gulfport', 'Pearl', 'Natchez', 'Ocean Springs', 'Starkville', 'Oxford', 'Gautier', 'Tupelo', 'Pascagoula'], 'New York': ['Nanuet', 'Mamaroneck', 'Bensonhurst', 'Bellmore', 'Cohoes', 'Kingston', 'Syracuse', 'Smithtown', 'East New York', 'Borough of Queens', 'Port Washington', 'Gloversville', 'Wantagh', 'Staten Island', 'Levittown', 'Huntington', 'Irondequoit', 'West Babylon', 'East Patchogue', 'New Rochelle', 'Centereach', 'Pearl River', 'Rochester', 'Hauppauge', 'Manhattan', 'Roosevelt', 'Huntington Station', 'Peekskill', 'New York City', 'North Bellmore', 'Valley Stream', 'Westbury', 'Selden', 'Mineola', 'Copiague', 'North Tonawanda', 'Spring Valley', 'Lynbrook', 'Eggertsville', 'North Babylon', 'Holtsville', 'Garden City', 'Jamestown', 'Merrick', 'Mount Vernon', 'Syosset', 'East Setauket', 'Lindenhurst', 'Dix Hills', 'Rotterdam', 'Saratoga Springs', 'Harrison', 'Rockville Centre', 'Central Islip', 'Mastic', 'Newburgh', 'Massapequa Park', 'North Bay Shore', 'White Plains', 'Depew', 'Lockport', 'Glen Cove', 'Beacon', 'Holbrook', 'Brooklyn', 'Cheektowaga', 'Oswego', 'Monsey', 'Sayville', 'Elmont', 'Scarsdale', 'Shirley', 'East Meadow', 'North Amityville', 'Kiryas Joel', 'Plattsburgh', 'Floral Park', 'Greenburgh', 'Binghamton', 'Amsterdam', 'Schenectady', 'Jamaica', 'West Albany', 'North Valley Stream', 'Utica', 'Seaford', 'Setauket-East Setauket', 'Commack', 'East Massapequa', 'Franklin Square', 'North Massapequa', 'Lake Ronkonkoma', 'Coney Island', 'Melville', 'Farmingville', 'Uniondale', 'Eastchester', 'Ithaca', 'Hempstead', 'Bethpage', 'Baldwin', 'Massapequa', 'Bay Shore', 'Freeport', 'Tonawanda', 'Poughkeepsie', 'Lackawanna', 'Woodmere', 'Niagara Falls', 'Albany', 'Islip', 'The Bronx', 'Cortland', 'West Islip', 'Rye', 'West Seneca', 'Long Island City', 'Yonkers', 'Deer Park', 'Elmira', 'Kings Park', 'East Northport', 'Amherst', 'Ronkonkoma', 'Coram', 'Ossining', 'Port Chester', 'New City', 'West Hempstead', 'Hicksville', 'Oceanside'], 'Oklahoma': ['Sand Springs', 'Shawnee', 'Chickasha', 'Mustang', 'Oklahoma City', 'Tahlequah', 'McAlester', 'Lawton', 'Altus', 'Ponca City', 'Claremore', 'Del City', 'Tulsa', 'Bartlesville', 'Muskogee', 'Broken Arrow', 'Ada', 'Jenks', 'Owasso', 'Moore', 'Ardmore', 'Midwest City', 'Stillwater', 'Bixby', 'Enid', 'Sapulpa', 'El Reno', 'Norman', 'Edmond', 'Duncan', 'Yukon', 'Bethany', 'Durant'], 'Maryland': ['Middle River', 'Hagerstown', 'White Oak', 'West Elkridge', 'Eldersburg', 'Rockville', 'Ellicott City', 'Crofton', 'Bethesda', 'Ilchester', 'North Bethesda', 'Calverton', 'Severn', 'Owings Mills', 'Fairland', 'Bel Air South', 'Camp Springs', 'Reisterstown', 'Dundalk', 'Olney', 'Glen Burnie', 'Cockeysville', 'Arbutus', 'Parole', 'Perry Hall', 'Randallstown', 'Wheaton', 'Redland', 'Severna Park', 'Catonsville', 'Essex', 'Elkton', 'Annapolis', 'Oxon Hill', 'Damascus', 'South Bel Air', 'Suitland', 'Langley Park', 'Silver Spring', 'Columbia', 'Lochearn', 'East Riverdale', 'Westminster', 'Elkridge', 'Frederick', 'Bel Air North', 'Potomac', 'Greenbelt', 'Green Haven', 'Chillum', 'Adelphi', 'Salisbury', 'Maryland City', 'Milford Mill', 'South Laurel', 'Baltimore', 'Waldorf', 'Woodlawn', 'North Bel Air', 'Takoma Park', 'Gaithersburg', 'Glassmanor', 'Rosedale', 'Lake Shore', 'Landover', 'Hyattsville', 'Odenton', 'College Park', 'Hillcrest Heights', 'Carney', 'Cumberland', 'North Potomac', 'Montgomery Village', 'Cloverly', 'Edgewood', 'Rossville', 'Pikesville', 'Parkville', 'Fort Washington', 'Beltsville', 'Ballenger Creek', 'Seabrook', 'Hunt Valley', 'Bowie', 'Towson', 'Aspen Hill'], 'Illinois': ['Carbondale', 'Naperville', 'Champaign', 'Rock Island', 'Godfrey', 'Vernon Hills', 'Orland Park', 'Huntley', 'Berwyn', 'Elgin', 'South Elgin', 'Bensenville', 'Crest Hill', 'Evanston', 'Villa Park', 'Urbana', 'Skokie', 'Cary', 'Fairview Heights', 'Lombard', 'Chicago', 'Belvidere', 'Geneva', 'South Holland', 'Goodings Grove', 'La Grange', 'Calumet City', 'Hoffman Estates', 'Palatine', 'Carol Stream', "O'Fallon", 'Pekin', 'Lake Forest', 'Melrose Park', 'Schaumburg', 'East Saint Louis', 'Sterling', 'Park Forest', 'Homer Glen', 'Matteson', 'Blue Island', 'Dolton', 'Shorewood', 'Cahokia', 'Ottawa', 'Des Plaines', 'Algonquin', 'Carpentersville', 'Addison', 'North Aurora', 'Plainfield', 'Lake in the Hills', 'Oak Lawn', 'Franklin Park', 'Morton Grove', 'Machesney Park', 'Libertyville', 'Gurnee', 'Northbrook', 'Glenview', 'Galesburg', 'Edwardsville', 'Evergreen Park', 'Maywood', 'Loves Park', 'Woodridge', 'Highland Park', 'Bolingbrook', 'Park Ridge', 'Tinley Park', 'Kankakee', 'North Peoria', 'Mundelein', 'Lisle', 'Buffalo Grove', 'Roselle', 'Hinsdale', 'Bartlett', 'Sycamore', 'Hanover Park', 'Lemont', 'Rockford', 'Rolling Meadows', 'Mattoon', 'Upper Alton', 'Alton', 'Romeoville', 'North Chicago', 'Belleville', 'Zion', 'Yorkville', 'Elmhurst', 'Prospect Heights', 'Alsip', 'Joliet', 'Arlington Heights', 'Bellwood', 'Glen Ellyn', 'Bridgeview', 'Darien', 'Grayslake', 'West Chicago', 'Round Lake', 'Granite City', 'East Moline', 'East Peoria', 'Bourbonnais', 'Batavia', 'Dixon', 'Bradley', 'Elk Grove Village', 'Crystal Lake', 'Deerfield', 'Oak Forest', 'DeKalb', 'Chicago Heights', 'Wilmette', 'Downers Grove', 'Country Club Hills', 'Elmwood Park', 'Normal', 'Mount Prospect', 'Mokena', 'Woodstock', 'Macomb', 'Round Lake Beach', 'Collinsville', 'Moline', 'Lake Zurich', 'Washington', 'Morton', 'Waukegan', 'Danville', 'Burbank', 'Palos Hills', 'McHenry', 'Cicero', 'New Lenox', 'Streamwood'], 'Idaho': ['Boise', 'Caldwell', 'Lewiston Orchards', 'Kuna', 'Post Falls', 'Rexburg', 'Nampa', 'Eagle', 'Meridian', "Coeur d'Alene", 'Twin Falls', 'Idaho Falls', 'Moscow', 'Pocatello'], 'Nevada': ['Las Vegas', 'Sun Valley', 'Boulder City', 'Spanish Springs', 'Pahrump', 'Fernley', 'Elko', 'Carson City', 'Whitney', 'Sparks', 'North Las Vegas', 'Summerlin South', 'Enterprise', 'Reno', 'Mesquite', 'Sunrise Manor'], 'Colorado': ['Denver', 'Commerce City', 'Southglenn', 'Highlands Ranch', 'Golden', 'Greeley', 'Brighton', 'Parker', 'Loveland', 'Littleton', 'Fountain', 'Windsor', 'Broomfield', 'Cimarron Hills', 'Louisville', 'Longmont', 'Canon City', 'Grand Junction', 'Montrose', 'Castle Rock', 'Wheat Ridge', 'Boulder', 'Pueblo', 'Arvada', 'Erie', 'Sherrelwood', 'Colorado Springs', 'Castlewood', 'Durango', 'Centennial', 'Columbine', 'Security-Widefield', 'Pueblo West', 'Ken Caryl', 'Fort Collins', 'Thornton', 'Northglenn'], 'Florida': ['Venice', 'Bartow', 'Edgewater', 'Allapattah', 'Hollywood', 'Richmond West', 'Pinecrest', 'Homestead', 'Meadow Woods', 'West Little River', 'Country Club', 'Winter Springs', 'Dunedin', 'Palm Valley', 'Naples', 'Casselberry', 'South Bradenton', 'Palm Coast', 'Merritt Island', 'Altamonte Springs', 'DeBary', 'Poinciana', 'Navarre', 'Royal Palm Beach', 'The Crossings', 'Tamarac', 'Fort Lauderdale', 'Carol City', 'Lake Magdalene', 'Titusville', 'Dania Beach', 'Brownsville', 'Largo', 'Jacksonville Beach', 'Ocala', 'Bonita Springs', 'Tampa', 'Bradenton', 'New Smyrna Beach', 'Pompano Beach', 'Miami Gardens', 'Lauderdale Lakes', 'Golden Gate', 'Tallahassee', 'Buenaventura Lakes', 'Brent', 'Crestview', 'Palmetto Bay', 'Coconut Creek', 'Saint Cloud', 'Pinewood', 'Ponte Vedra Beach', 'Pinellas Park', 'Maitland', 'Fort Walton Beach', 'Valrico', 'Cocoa', 'Opa-locka', 'South Miami Heights', 'Ormond Beach', 'Pembroke Pines', 'Lake Worth Corridor', 'Cutler Bay', 'Southchase', 'Keystone', 'Fruit Cove', 'Lauderhill', 'Vero Beach South', 'Ensley', 'Kissimmee', 'Fountainebleau', 'Seminole', "Town 'n' Country", 'Ojus', 'Kendale Lakes', 'Three Lakes', 'Plantation', 'Holiday', 'Wellington', 'Egypt Lake-Leto', 'Miami Beach', 'Temple Terrace', 'Apopka', 'Immokalee', 'Lehigh Acres', 'Oakland Park', 'Sunset', 'Clermont', 'Kendall', 'North Lauderdale', 'East Lake', 'Riverview', 'Rockledge', 'Winter Haven', 'Lakeside', 'Greater Northdale', 'Golden Glades', 'Fort Myers', 'Jupiter', 'Norland', 'Stuart', 'Vero Beach', 'East Pensacola Heights', 'Delray Beach', 'Key West', 'Riviera Beach', 'Spring Hill', 'Boynton Beach', 'Greenacres City', "Land O' Lakes", 'Palm Beach Gardens', 'Hallandale Beach', 'Carrollwood', 'West and East Lealman', 'Winter Garden', 'Eustis', 'Wright', 'Davie', 'Punta Gorda', 'Ferry Pass', 'Lakeland', 'Lake Butler', 'Cantonment', 'Alafaya', 'Deerfield Beach', 'Pace', 'West Palm Beach', 'Iona', 'Country Walk', 'Fort Pierce', 'Citrus Park', 'Bloomingdale', 'Miramar', 'Coral Gables', 'Lake Worth', 'Daytona Beach', 'Flagami', 'Coconut Grove', 'Palm City', 'North Fort Myers', 'North Miami', 'Oviedo', 'Cutler', 'Port Saint Lucie', 'Orlando', 'Carrollwood Village', 'West Pensacola', 'Cutler Ridge', 'Haines City', 'Cape Coral', 'Miami Lakes', 'Bellview', 'Clearwater', 'Plant City', 'Myrtle Grove', 'Wesley Chapel', 'Punta Gorda Isles', 'Boca Del Mar', 'Pine Hills', 'San Carlos Park', 'Bayshore Gardens', 'Westchase', 'Lutz', 'West Melbourne', 'Sebastian', 'East Lake-Orient Park', 'Sunrise', 'Melbourne', 'Aventura', 'Palm Bay', 'Saint Petersburg', 'Glenvar Heights', 'Princeton', 'Sun City Center', 'Ives Estates', 'Pensacola', 'Safety Harbor', 'Tamiami', 'Coral Terrace', 'North Miami Beach', 'Winter Park', 'Coral Springs', 'Sanford', 'Westchester', 'Port Orange', 'Tarpon Springs', 'Hialeah', 'Ruskin', 'Jasmine Estates', 'Florida Ridge', 'Wekiwa Springs', 'Cooper City', 'Miami', 'Deltona', 'Margate', 'Sarasota', 'The Hammocks', 'Belle Glade', 'Panama City', 'Port Charlotte', 'DeLand', 'Bayonet Point', 'Lealman', 'Doral', 'Ocoee', 'North Port', 'Boca Raton', 'Leisure City', 'Hialeah Gardens', 'Palm Harbor', 'The Villages', 'University', 'Sunny Isles Beach', 'Leesburg', 'Weston', 'Estero', 'Lynn Haven'], 'Texas': ['Dallas', 'Brownwood', 'Harlingen', 'Ennis', 'Cloverleaf', 'Farmers Branch', 'Cedar Hill', 'Eagle Pass', 'Plainview', 'Angleton', 'Corpus Christi', 'Bryan', 'Harker Heights', 'Colleyville', 'Amarillo', 'Coppell', 'Channelview', 'Fort Hood', 'Euless', 'Haltom City', 'Edinburg', 'Socorro Mission Number 1 Colonia', 'Beaumont', 'Aldine', 'Balch Springs', 'Flower Mound', 'Alamo', 'Alvin', 'Atascocita', 'Georgetown', 'Denison', 'Del Rio', 'Alice', 'Corinth', 'Groves', 'Garland', 'Big Spring', 'Cedar Park', 'Friendswood', 'Pampa', 'Gainesville', 'West Odessa', 'Socorro', 'Odessa', 'Burleson', 'San Angelo', 'El Paso', 'Copperas Cove', 'Brushy Creek', 'Abilene', 'Bellaire', 'Donna', 'Gatesville', 'Corsicana', 'Houston', 'College Station', 'DeSoto', 'Cinco Ranch', 'Grand Prairie', 'Horizon City', 'Benbrook', 'Galveston', 'Converse', 'Grapevine', 'Cleburne', 'Conroe', 'Hurst', 'Lubbock', 'Cibolo', 'Highland Village', 'Allen', 'Frisco', 'Brenham', 'Fort Worth', 'Humble', 'Baytown', 'Canyon Lake', 'Greenville', 'Fresno', 'Midland', 'Hereford', 'Denton', 'Duncanville'], 'Arkansas': ['Benton', 'Pine Bluff', 'Bentonville', 'Forrest City', 'El Dorado', 'Texarkana', 'Russellville', 'Paragould', 'Bella Vista', 'Jonesboro', 'North Little Rock', 'Conway', 'Little Rock', 'Cabot', 'Searcy', 'Van Buren', 'Jacksonville', 'Rogers', 'Hot Springs National Park', 'Springdale', 'Bryant', 'Maumelle', 'Fort Smith', 'Blytheville', 'Siloam Springs', 'Hot Springs', 'West Memphis'], 'Arizona': ['Lake Havasu City', 'Queen Creek', 'San Luis', 'Apache Junction', 'Surprise', 'Scottsdale', 'Casas Adobes', 'Rio Rico', 'Payson', 'Sun City West', 'Yuma', 'Flowing Wells', 'Fortuna Foothills', 'Chandler', 'Eloy', 'Tucson', 'Casa Grande', 'Tempe', 'Nogales', 'Catalina Foothills', 'Phoenix', 'Douglas', 'Sahuarita', 'Bullhead City', 'Drexel Heights', 'Fountain Hills', 'Anthem', 'Tempe Junction', 'El Mirage', 'Sierra Vista', 'Flagstaff', 'Peoria', 'Maricopa', 'Prescott Valley', 'Mesa', 'Avondale', 'Oro Valley', 'Gilbert', 'Green Valley', 'Goodyear', 'San Tan Valley', 'Kingman', 'Tanque Verde', 'Sun City', 'Prescott', 'Buckeye', 'Marana'], 'Tennessee': ['New South Memphis', 'Tullahoma', 'Lavergne', 'Maryville', 'Lebanon', 'Murfreesboro', 'East Brainerd', 'Nashville', 'Hendersonville', 'Kingsport', 'Chattanooga', 'Mount Juliet', 'Knoxville', 'East Chattanooga', 'Goodlettsville', 'Greeneville', 'Johnson City', 'Collierville', 'Gallatin', 'Germantown', 'Farragut', 'Dyersburg', 'East Ridge', 'Brentwood Estates', 'Cookeville', 'Memphis', 'Oak Ridge'], 'South Carolina': ['North Augusta', 'Goose Creek', 'Greer', 'Summerville', 'Seven Oaks', 'Taylors', 'Socastee', 'North Charleston', 'Myrtle Beach', 'Hilton Head Island', 'Simpsonville', 'Anderson', 'Greenwood', 'Wade Hampton', 'Easley', 'Aiken', 'Hanahan', 'Saint Andrews', 'Mauldin', 'Spartanburg', 'Charleston', 'Rock Hill', 'Sumter'], 'Massachusetts': ['Methuen', 'Natick', 'Shrewsbury', 'Brockton', 'Rockland', 'Yarmouth', 'Westfield', 'South Peabody', 'Everett', 'Taunton', 'Swansea', 'Melrose', 'Sudbury', 'South Hadley', 'Agawam', 'Jamaica Plain', 'Billerica', 'Amesbury', 'Wellesley', 'Worcester', 'Ludlow', 'Acton', 'Haverhill', 'East Longmeadow', 'Dedham', 'Palmer', 'Easthampton', 'Framingham Center', 'Beverly Cove', 'Easton', 'Belmont', 'Fall River', 'Norton', 'Stoneham', 'Longmeadow', 'Lawrence', 'Framingham', 'Chelmsford', 'Lynn', 'Auburn', 'Grafton', 'Springfield', 'New Bedford', 'Wakefield', 'Gloucester', 'Leominster', 'West Springfield', 'Newburyport', 'Chicopee', 'Milton', 'Danvers', 'Winthrop', 'Southbridge', 'Saugus', 'Attleboro', 'Milford', 'Franklin', 'Reading', 'Marblehead', 'Boston', 'South Boston', 'Waltham', 'Amherst Center', 'Holden', 'Westford', 'Ashland', 'North Chicopee', 'Barnstable', 'Northampton', 'Randolph', 'Malden', 'Quincy', 'Lowell', 'Hanover', 'Somerville', 'Braintree', 'Woburn', 'Weymouth', 'Dracut', 'Brookline', 'Chelsea', 'Peabody', 'Stoughton', 'Marlborough', 'Fairhaven', 'Pittsfield', 'Cambridge', 'Watertown', 'Holyoke', 'Needham', 'Tewksbury', 'Abington', 'Beverly'], 'Washington': ['University Place', 'Parkland', 'Aberdeen', 'Lynnwood', 'Monroe', 'Mill Creek', 'Bothell', 'Mukilteo', 'Bremerton', 'Covington', 'Orchards', 'Cottage Lake', 'Shoreline', 'Mercer Island', 'Lake Stevens', 'North Creek', 'Longview', 'Five Corners', 'West Lake Stevens', 'Kennewick', 'Bryn Mawr-Skyway', 'Lacey', 'Ellensburg', 'Spokane Valley', 'Silverdale', 'Salmon Creek', 'City of Sammamish', 'Centralia', 'Edmonds', 'East Hill-Meridian', 'Kent', 'Frederickson', 'Sammamish', 'South Hill', 'Pasco', 'Yakima', 'SeaTac', 'Opportunity', 'Camas', 'Martha Lake', 'Hazel Dell', 'Moses Lake', 'Issaquah', 'Maple Valley', 'Silver Firs', 'Bonney Lake', 'Pullman', 'Tacoma', 'Sunnyside', 'Olympia', 'Walla Walla', 'Burien', 'Lakewood', 'Oak Harbor', 'Puyallup', 'Arlington', 'Renton', 'Redmond', 'Richland', 'Bainbridge Island', 'Battle Ground', 'Port Angeles', 'Tumwater', 'Vancouver', 'Union Hill-Novelty Hill', 'Bellingham', 'Inglewood-Finn Hill', 'Wenatchee', 'Spokane', 'Marysville', 'Tukwila', 'Seattle', 'Spanaway', 'Kenmore', 'Fairwood', 'Graham', 'Mountlake Terrace', 'Anacortes', 'Federal Way', 'West Lake Sammamish', 'Kirkland'], 'Indiana': ['Muncie', 'Carmel', 'Vincennes', 'Mishawaka', 'Clarksville', 'Crown Point', 'Hobart', 'Valparaiso', 'Evansville', 'Fishers', 'LaPorte', 'South Bend', 'Griffith', 'Crawfordsville', 'Shelbyville', 'Brownsburg', 'West Lafayette', 'Schererville', 'East Chicago', 'Munster', 'Jasper', 'New Albany', 'Noblesville', 'Fairfield Heights', 'Kokomo', 'Portage', 'Fort Wayne', 'Broad Ripple', 'Terre Haute', 'Highland', 'Bloomington', 'Seymour', 'Logansport', 'Gary', 'Elkhart', 'Granger', 'Michigan City', 'Hammond', 'Indianapolis', 'Merrillville', 'Goshen', 'Dyer', 'Jeffersonville'], 'Wisconsin': ['North La Crosse', 'Racine', 'Stevens Point', 'De Pere', 'Kenosha', 'Menomonee Falls', 'Menasha', 'Wausau', 'Waukesha', 'New Berlin', 'Mequon', 'Sun Prairie', 'La Crosse', 'Onalaska', 'Fond du Lac', 'West Bend', 'Ashwaubenon', 'Eau Claire', 'Fitchburg', 'Sheboygan', 'Appleton', 'Cudahy', 'Oshkosh', 'Caledonia', 'Janesville', 'Milwaukee', 'Wisconsin Rapids', 'Manitowoc', 'Howard', 'Greenfield', 'Pleasant Prairie', 'Kaukauna', 'Beloit', 'Neenah', 'Marshfield', 'Oconomowoc', 'Muskego', 'Middleton', 'Brookfield', 'South Milwaukee', 'Beaver Dam', 'Menomonie', 'Wauwatosa', 'Oak Creek', 'Superior', 'Green Bay', 'West Allis'], 'Ohio': ['Fairview Park', 'Troy', 'East Cleveland', 'Newark', 'Xenia', 'North Olmsted', 'Huber Heights', 'Bay Village', 'Cincinnati', 'North Royalton', 'Vandalia', 'Avon Center', 'Maple Heights', 'Defiance', 'Grove City', 'Marion', 'Wooster', 'Findlay', 'Willoughby', 'South Euclid', 'Lancaster', 'Gahanna', 'Riverside', 'Rocky River', 'Akron', 'Broadview Heights', 'Green', 'Aurora', 'Eastlake', 'Strongsville', 'Tiffin', 'Perrysburg', 'Avon', 'Sandusky', 'New Philadelphia', 'Beavercreek', 'Norwood', 'Twinsburg', 'Massillon', 'Westlake', 'Pickerington', 'Dayton', 'Sidney', 'Upper Arlington', 'North Ridgeville', 'Hudson', 'Delaware', 'Zanesville', 'Piqua', 'Steubenville', 'Painesville', 'Ashtabula', 'Parma Heights', 'Mentor', 'Westerville', 'Bowling Green', 'Streetsboro', 'Kettering', 'Tallmadge', 'Alliance', 'Warren', 'Hamilton', 'Miamisburg', 'Oregon', 'Fairborn', 'Medina', 'Austintown', 'Parma', 'Wadsworth', 'Mansfield', 'Reynoldsburg', 'Toledo', 'Lima', 'Mayfield Heights', 'Barberton', 'Boardman', 'Trotwood', 'Garfield Heights', 'Whitehall', 'Avon Lake', 'Berea', 'Sylvania', 'Lorain', 'Stow', 'Elyria', 'Mason', 'North Canton', 'Hilliard', 'Solon', 'Cuyahoga Falls', 'Shaker Heights', 'Fairfield', 'Middleburg Heights', 'Youngstown', 'Brook Park', 'Cleveland', 'Euclid', 'Niles', 'Springboro'], 'Missouri': ['Wentzville', 'Fort Leonard Wood', 'Clayton', 'Chesterfield', 'Spanish Lake', 'Warrensburg', 'Webster Groves', 'Ferguson', 'Belton', 'East Independence', 'Cape Girardeau', 'Raymore', 'Maryland Heights', 'Hannibal', 'Affton', 'Ballwin', 'Saint Charles', 'Liberty', 'Sikeston', 'Mehlville', 'Kirksville', 'Jefferson City', 'St. Louis', 'Wildwood', 'Oakville', 'Raytown', 'University City', 'Hazelwood', 'Lemay', 'Ozark', 'Gladstone', 'Grandview', 'Overland', 'Kirkwood', 'Saint Joseph', 'Blue Springs', 'Creve Coeur', 'Concord', 'Arnold', 'Sedalia', "Lee's Summit", 'Nixa', 'Rolla', 'Saint Peters', 'Florissant', 'Joplin', 'Poplar Bluff'], 'New Jersey': ['Livingston', 'Pennsauken', 'West New York', 'Maplewood', 'Montclair', 'Somerset', 'Toms River', 'Colonia', 'Rahway', 'Madison', 'Parsippany', 'Ridgewood', 'Point Pleasant', 'Bridgewater', 'Marlboro', 'Willingboro', 'Cliffside Park', 'Edison', 'Summit', 'Ewing', 'Paterson', 'Jersey City', 'New Milford', 'Nutley', 'Tinton Falls', 'Hoboken', 'Mahwah', 'Piscataway', 'West Orange', 'South Vineland', 'Sicklerville', 'Union City', 'Bloomfield', 'Old Bridge', 'Hopatcong Hills', 'Irvington', 'Iselin', 'Asbury Park', 'Hopatcong', 'Clifton', 'Kearny', 'Woodbridge', 'Warren Township', 'North Bergen', 'West Milford', 'Bridgeton', 'Atlantic City', 'Secaucus', 'Cranford', 'Orange', 'Cherry Hill', 'Teaneck', 'Englewood', 'Bayonne', 'Union', 'Perth Amboy', 'Hackensack', 'Garfield', 'Hillside', 'Lodi', 'New Brunswick', 'Maple Shade', 'Glassboro', 'Fords', 'Pleasantville', 'Carteret', 'Paramus', 'Passaic', 'Fair Lawn', 'South Plainfield', 'East Orange', 'South Orange', 'Linden', 'Palisades Park', 'Lindenwold', 'Wayne', 'Sayreville Junction', 'Camden', 'North Arlington', 'Sayreville', 'Wyckoff', 'Mount Laurel', 'Morristown', 'Rutherford', 'Bergenfield', 'South River', 'Vineland', 'Scotch Plains', 'Millville', 'Avenel', 'Dumont', 'Long Branch', 'Fort Lee', 'South Old Bridge', 'Williamstown', 'Elizabeth', 'Lyndhurst', 'Ocean Acres', 'East Brunswick', 'North Plainfield'], 'Louisiana': ['New Iberia', 'Marrero', 'Prairieville', 'Lafayette', 'Natchitoches', 'Chalmette', 'Gretna', 'Shenandoah', 'Ruston', 'Terrytown', 'Bossier City', 'Opelousas', 'Metairie Terrace', 'Baton Rouge', 'Estelle', 'Central', 'Bayou Cane', 'Metairie', 'Harvey', 'Lake Charles', 'Shreveport', 'New Orleans', 'Kenner', 'Sulphur', 'Alexandria', 'Slidell', 'Houma', 'Laplace'], 'North Carolina': ['Greensboro', 'Cornelius', 'Durham', 'Kinston', 'Kernersville', 'Holly Springs', 'Carrboro', 'Indian Trail', 'Rocky Mount', 'Matthews', 'Garner', 'Mooresville', 'Henderson', 'Raleigh', 'Albemarle', 'Gastonia', 'Wake Forest', 'Goldsboro', 'High Point', 'West Raleigh', 'Fuquay-Varina', 'Fort Bragg', 'Hope Mills', 'Lumberton', 'Thomasville', 'Morrisville', 'Mint Hill', 'New Bern', 'Charlotte', 'Eden', 'Huntersville', 'Clemmons', 'Boone', 'Roanoke Rapids', 'Statesville', 'Asheboro', 'Wilson', 'Morganton', 'Asheville', 'Apex', 'Elizabeth City', 'Lenoir', 'Hickory', 'Kannapolis', 'Havelock', 'Wilmington', 'Laurinburg', 'Chapel Hill', 'Winston-Salem'], 'Kansas': ['Emporia', 'Topeka', 'Lenexa', 'Hays', 'Gardner', 'Junction City', 'Prairie Village', 'Derby', 'Dodge City', 'Great Bend', 'Liberal', 'Hutchinson', 'Olathe', 'Salina', 'Newton', 'Leavenworth', 'Overland Park', 'Kansas City', 'Leawood', 'Wichita', 'Pittsburg'], 'West Virginia': ['Wheeling', 'Weirton', 'Weirton Heights'], 'Connecticut': ['Irving', 'Branford', 'West Torrington', 'West Haven', 'Wethersfield', 'Ansonia', 'City of Milford (balance)', 'Wolcott', 'Willimantic', 'Windham', 'Westport', 'Cheshire', 'Bridgeport', 'Wallingford Center', 'West Hartford', 'Wilton'], 'Alabama': ['Prattville', 'Homewood', 'Center Point', 'Trussville', 'Talladega', 'Florence', 'Montgomery', 'Dothan', 'Dixiana', 'Vestavia Hills', 'Mountain Brook', 'Gadsden', 'Pelham', 'Birmingham', 'Huntsville', 'Bessemer', 'Prichard', 'Tuscaloosa', 'Phenix City', 'Opelika', 'Hueytown', 'Northport', 'Fairhope', 'Tillmans Corner', 'Mobile', 'East Florence', 'Daphne', 'Hoover'], 'Oregon': ['Aloha', 'Oak Grove', 'Lake Oswego', 'Grants Pass', 'Woodburn', 'Four Corners', 'McMinnville', 'Tigard', 'Troutdale', 'Hillsboro', 'Tualatin', 'Newberg', 'Coos Bay', 'Gresham', 'Milwaukie', 'Roseburg', 'Altamont', 'Central Point', 'Hermiston', 'Klamath Falls', 'Sherwood', 'Wilsonville', 'Canby', 'Corvallis', 'Medford', 'Salem', 'Forest Grove', 'Eugene', 'Lents', 'Oregon City', 'Hayesville', 'Portland', 'Pendleton', 'Bend', 'West Linn', 'Keizer'], 'Georgia': ['Dunwoody', 'Carrollton', 'Wilmington Island', 'Americus', 'Augusta', 'Acworth', 'Lithia Springs', 'Milledgeville', 'Columbus', 'Calhoun', 'Newnan', 'St. Marys', 'Hinesville', 'Douglasville', 'Statesboro', 'Roswell', 'Fayetteville', 'McDonough', 'Macon', 'Smyrna', 'Dalton', 'Sandy Springs', 'Snellville', 'Evans', 'Candler-McAfee', 'Marietta', 'Brookhaven', 'Tifton', 'Lawrenceville', 'Alpharetta', 'Atlanta', 'Savannah', 'East Point', 'North Decatur', 'Decatur', 'Athens', 'Pooler', 'Kingsland', 'Sugar Hill', 'Canton', 'Griffin', 'Kennesaw', 'Peachtree City', 'Conyers', 'Belvedere Park', 'Rome', 'Valdosta', 'Stockbridge', 'Warner Robins', 'Tucker', 'Redan', 'Johns Creek', 'Suwanee', 'Forest Park', 'Cartersville', 'Brunswick', 'Mableton', 'Riverdale', 'North Druid Hills'], 'North Dakota': ['Grand Forks', 'Minot', 'Fargo', 'West Fargo', 'Dickinson', 'Bismarck', 'Mandan'], 'Iowa': ['Cedar Falls', 'Marshalltown', 'Council Bluffs', 'Cedar Rapids', 'Waterloo', 'West Des Moines', 'Iowa City', 'Ankeny', 'Urbandale', 'Muscatine', 'Fort Dodge', 'Mason City', 'Ames', 'Clive', 'Coralville', 'Bettendorf', 'Des Moines', 'Dubuque', 'Johnston', 'Sioux City', 'Davenport', 'Ottumwa'], 'Pennsylvania': ['Hazleton', 'Chester', 'State College', 'Upper Saint Clair', 'Murrysville', 'Radnor', 'Limerick', 'West Chester', 'Chambersburg', 'Norristown', 'Scranton', 'New Castle', 'Harrisburg', 'Whitehall Township', 'Cranberry Township', 'McKeesport', 'Johnstown', 'King of Prussia', 'Lansdale', 'Pottstown', 'Altoona', 'Mountain Top', 'Allentown', 'Drexel Hill', 'Philadelphia', 'Phoenixville', 'Williamsport', 'Monroeville', 'Wilkes-Barre', 'Back Mountain', 'Pittsburgh', 'Plum', 'Allison Park', 'Carlisle', 'Willow Grove', 'Bethlehem', 'Penn Hills', 'York', 'Bethel Park', 'Wilkinsburg', 'West Mifflin', 'Mount Lebanon', 'Hermitage'], 'Michigan': ['Burton', 'Ferndale', 'Southfield', 'Eastpointe', 'Lincoln Park', 'Dearborn Heights', 'Detroit', 'Flint', 'Sterling Heights', 'Madison Heights', 'Owosso', 'Jackson', 'Battle Creek', 'West Bloomfield Township', 'Hamtramck', 'Ypsilanti', 'Rochester Hills', 'Redford', 'Livonia', 'Bay City', 'Taylor', 'Hazel Park', 'Grandville', 'Jenison', 'Mount Clemens', 'Saint Clair Shores', 'Westland', 'Novi', 'Waverly', 'Saginaw', 'Farmington Hills', 'Mount Pleasant', 'Okemos', 'Kentwood', 'Holland', 'Holt', 'Shelby', 'Haslett', 'Iron River', 'Muskegon', 'Wyandotte', 'Oak Park', 'East Lansing', 'Wyoming', 'Grand Rapids', 'Adrian', 'Romulus', 'Forest Hills', 'Grosse Pointe Woods', 'Waterford', 'Trenton', 'Pontiac', 'Norton Shores', 'Ann Arbor', 'Allendale', 'Lansing', 'Marquette', 'Southgate', 'Port Huron', 'Kalamazoo', 'Dearborn', 'Allen Park', 'Auburn Hills', 'Walker', 'Royal Oak'], 'Rhode Island': ['West Warwick', 'North Kingstown', 'Warwick', 'Newport', 'Cranston', 'Providence', 'Westerly', 'Bristol', 'North Providence', 'Central Falls', 'Middletown', 'Smithfield', 'Coventry', 'Woonsocket', 'Pawtucket', 'Barrington', 'East Providence'], 'Utah': ['Centerville', 'American Fork', 'Millcreek', 'Magna', 'Herriman', 'Logan', 'Orem', 'Salt Lake City', 'West Valley City', 'Kaysville', 'South Jordan Heights', 'East Millcreek', 'North Salt Lake', 'South Salt Lake', 'Lehi', 'Sandy Hills', 'West Jordan', 'South Ogden', 'Brigham City', 'Midvale', 'Saint George', 'Roy', 'Clearfield', 'Farmington', 'Sandy City', 'Holladay', 'Cottonwood Heights', 'Springville', 'Ogden', 'North Ogden', 'Layton', 'Taylorsville', 'Draper', 'Eagle Mountain', 'Spanish Fork', 'Provo', 'Pleasant Grove', 'South Jordan', 'Cedar City', 'Kearns', 'Riverton', 'Bountiful', 'Tooele'], 'Maine': ['South Portland', 'Bangor', 'South Portland Gardens', 'Lewiston', 'Westbrook', 'Waterville', 'Saco', 'West Scarborough', 'Biddeford'], 'Hawaii': ['Kihei', 'Waipahu', 'Kaneohe', 'Kahului', 'Pearl City', 'Mililani Town', 'Honolulu', 'Wahiawa', 'Wailuku', 'Kailua', 'Schofield Barracks', 'Makakilo City', 'Hilo', 'Ewa Gentry', 'Makakilo'], 'New Mexico': ['South Valley', 'Albuquerque', 'Carlsbad', 'Alamogordo', 'Rio Rancho', 'Santa Fe', 'Las Cruces', 'Gallup', 'Enchanted Hills', 'Hobbs'], 'Kentucky': ['Paducah', 'Erlanger', 'Winchester', 'Hopkinsville', 'Radcliff', 'Newburg', 'Frankfort', 'Lexington-Fayette', 'Richmond', 'Shively', 'Saint Matthews', 'Jeffersontown', 'Valley Station', 'Pleasure Ridge Park', 'Okolona', 'Independence', 'Murray', 'Nicholasville', 'Highview', 'Burlington', 'Meads', 'Lexington', 'Owensboro', 'Ironville', 'Elizabethtown', 'Madisonville', 'Fort Thomas', 'Fern Creek'], 'Minnesota': ['Austin', 'Lino Lakes', 'Moorhead', 'Columbia Heights', 'Blaine', 'Oakdale', 'Chanhassen', 'New Hope', 'Woodbury', 'Edina', 'Chaska', 'Fridley', 'Albert Lea', 'Lakeville', 'Owatonna', 'Red Wing', 'Mankato', 'Minnetonka Mills', 'Ham Lake', 'Shoreview', 'Inver Grove Heights', 'New Brighton', 'Brooklyn Center', 'Prior Lake', 'Saint Paul', 'Champlin', 'Plymouth', 'Sartell', 'Saint Michael', 'Anoka', 'Willmar', 'Coon Rapids', 'Golden Valley', 'Minneapolis', 'Cottage Grove', 'Maple Grove', 'Hopkins', 'Duluth', 'West Saint Paul', 'Crystal', 'South Saint Paul', 'Brooklyn Park', 'Forest Lake', 'Shakopee', 'Hibbing', 'White Bear Lake', 'Faribault', 'Saint Louis Park', 'Richfield', 'Winona', 'Burnsville', 'Buffalo', 'Rosemount', 'Minnetonka', 'Apple Valley', 'Elk River', 'Andover', 'Ramsey', 'West Coon Rapids', 'Northfield', 'Eden Prairie', 'Savage', 'Eagan'], 'Nebraska': ['Norfolk', 'Papillion', 'North Platte', 'Omaha', 'Grand Island', 'Hastings', 'Lincoln', 'Scottsbluff', 'Bellevue', 'Kearney', 'La Vista'], 'Montana': ['Great Falls', 'Kalispell', 'Butte', 'Helena', 'Billings', 'Butte-Silver Bow (Balance)', 'Missoula', 'Bozeman'], 'Alaska': ['Juneau', 'Fairbanks', 'Anchorage', 'Eagle River', 'Badger'], 'South Dakota': ['Rapid City', 'Brookings', 'Mitchell', 'Sioux Falls'], 'Virginia': ['Fort Hunt', 'Oak Hill'], 'New Hampshire': ['Nashua', 'Bedford', 'Laconia', 'Merrimack', 'Manchester', 'Derry', 'Derry Village', 'East Concord', 'Portsmouth', 'Keene'], 'Wyoming': ['Gillette', 'Rock Springs', 'Cheyenne', 'Laramie', 'Casper', 'Sheridan'], 'Vermont': ['South Burlington', 'Colchester', 'Rutland'], 'Delaware': ['Bear', 'Dover'], 'District of Columbia': ['Washington, D.C.']}
    if df.name.strip().lower().startswith('lat') or df.name.strip().lower().startswith('long') or df.name.strip().lower().startswith('经度') or df.name.strip().lower().startswith('纬度'):
        df_type["type"] = "geographical"
        df_type["hierarchy"] = 'latitude and longtitude'
        df_type["values"] = df.fillna('unknown').unique().tolist()
        df_type['isPostCode']=False
        if df.name.strip().lower().startswith('lat') or df.name.strip().lower().startswith('经度'):
            df_type['subtype']='latitude'
        elif df.name.strip().lower().startswith('long') or df.name.strip().lower().startswith('纬度'):  
            df_type['subtype']='longtitude'
    elif any(i in df.name.lower() for i in ['zipcode','postcode','zip code','post code','areacode', 'area code']):
        df_type["type"] = "geographical"
        df_type["values"] = df.fillna('unknown').unique().tolist()
        df_type['hierarchy']='postcode'
        df_type['isPostCode']= True
        if df.dtype =='int64':
            if all(len(str(i))==5 for i in df):
                df_type['subtype']='us'
            elif all(len(str(i))==6 for i in df):
                df_type['subtype']='china'
            else: 
                df_type['subtype']='world'
        else:
            df_type['subtype']='world'
    elif 'state' in df.name.lower() or '省' in df.name.lower() or 'province' in df.name.lower() or '州' in df.name.lower():
        df_type["type"] = "geographical"
        df_type["values"] = df.fillna('unknown').unique().tolist()
        df_type['isPostCode']=False
        try:
            df=df.str.strip()
        except:
            print('strip_fail')
        df_type['hierarchy']='state'
        if type(df.dropna().any()) is str and (any(df[1] in x for x in _China.keys()) or any(df[1] in x for x in _China1.values())):
            df_type['subtype']='china'
        elif type(df.dropna().any()) is str and any(df[1].strip() in x for x in _US.keys()):
            df_type['subtype']='usa'
        elif type(df.dropna().any()) is str:
            df_type['subtype']='world'   
        else:
            df_type['subtype']='unknown'   
    elif 'area' in df.name.lower() or 'region' in df.name.lower() or '地区' in df.name.lower():
        df_type["type"] = "geographical"
        df_type["values"] = df.fillna('unknown').unique().tolist()
        df_type['isPostCode']=False
        try:
            df=df.str.strip()
        except:
            print('strip_fail')
        df_type['hierarchy']='city'
        if type(df.dropna().any()) is str and any(df[1] in x for x in numpy.concatenate(list(_China.values()))) :
            df_type['subtype']='china'
        elif type(df.dropna().any()) is str and any(df[1] in x for x in numpy.concatenate(list(_US.values()))):
            df_type['subtype']='usa'
        elif type(df.dropna().any()) is str:
            df_type['subtype']='world'   
        else:
            df_type['subtype']='unknown'   
    elif ('city' in df.name.lower() and 'icity' not in df.name.lower()) or '市' in df.name.lower():
        df_type["type"] = "geographical"
        df_type["values"] = df.fillna('unknown').unique().tolist()
        df_type['isPostCode']=False
        try:
            df=df.str.strip()
        except:
            print('strip_fail')
        df_type['hierarchy']='city'
        if type(df.dropna().any()) is str and any(df[1] in x for x in numpy.concatenate(list(_China.values()))):
            df_type['subtype']='china'
        elif type(df.dropna().any()) is str and any(df[1] in x for x in numpy.concatenate(list(_US.values()))):
            df_type['subtype']='usa'
        elif type(df.dropna().any()) is str:
            df_type['subtype']='world'   
        else:
            df_type['subtype']='unknown'   
    elif 'suburb' in df.name.lower() or '区' in df.name.lower():
        df_type["type"] = "geographical"
        df_type["values"] = df.fillna('unknown').unique().tolist()
        df_type['isPostCode']=False
        try:
            df=df.str.strip()
        except:
            print('strip_fail')
        df_type['hierarchy']='suburb'
        if type(df.dropna().any()) is str and any(df[1] in x for x in numpy.concatenate(list(_China.values()))):
            df_type['subtype']='china'
        elif type(df.dropna().any()) is str and any(df[1] in x for x in numpy.concatenate(list(_US.values()))):
            df_type['subtype']='usa'
        elif type(df.dropna().any()) is str:
            df_type['subtype']='world'   
        else:
            df_type['subtype']='unknown'   
    else:
        if _countries(df[0]):
            df_type["type"] = "geographical"
            df_type['subtype']='world'
            df_type['hierarchy']='country'
            df_type['isPostCode']=False
            df_type["values"] = df.fillna('unknown').unique().tolist()
        elif df[0] in [i.alpha_2 for i in list(pycountry.countries)] or df[0] in [i.alpha_3 for i in list(pycountry.countries)]:
            df_type["type"] = "geographical"
            df_type['subtype']='world'
            df_type['hierarchy']='country'
            df_type['isPostCode']=False
            df_type["values"] = df.fillna('unknown').unique().tolist()
        else:
            df_type["type"] = "categorical"
            df_type["subtype"] = df.name 
            df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist())) 

    return df_type

def _countries(name):
    _countries = ['afghanistan', 'aland islands', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas (the)', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia (plurinational state of)', 'bonaire, sint eustatius and saba', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory (the)', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cabo verde', 'cambodia', 'cameroon', 'canada', 'cayman islands (the)', 'central african republic (the)', 'chad', 'chile', 'china', 'christmas island', 'cocos (keeling) islands (the)', 'colombia', 'comoros (the)', 'congo (the democratic republic of the)', 'congo (the)', 'cook islands (the)', 'costa rica', "cote d'ivoire", 'croatia', 'cuba', 'curacao', 'cyprus', 'czechia', 'denmark', 'djibouti', 'dominica', 'dominican republic (the)', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands (the) [malvinas]', 'faroe islands (the)', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories (the)', 'gabon', 'gambia (the)', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdonald islands', 'holy see (the)', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran (islamic republic of)', 'iraq', 'ireland', 'isle of man', 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', "korea (the democratic people's republic of)", 'korea (the republic of)', 'kuwait', 'kyrgyzstan', "lao people's democratic republic (the)", 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia (the former yugoslav republic of)', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands (the)', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia (federated states of)', 'moldova (the republic of)', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands (the)', 'new caledonia', 'new zealand', 'nicaragua', 'niger (the)', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands (the)', 'norway', 'oman', 'pakistan', 'palau', 'palestine, state of', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines (the)', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'reunion', 'romania', 'russian federation (the)', 'rwanda', 'saint barthelemy', 'saint helena, ascension and tristan da cunha', 'saint kitts and nevis', 'saint lucia', 'saint martin (french part)', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten (dutch part)', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and the south sandwich islands', 'south sudan', 'spain', 'sri lanka', 'sudan (the)', 'suriname', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan (province of china)', 'tajikistan', 'tanzania, united republic of', 'thailand', 'timor-leste', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands (the)', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates (the)', 'united kingdom of great britain and northern ireland (the)','USA','US','UK','united states minor outlying islands (the)', 'united states of america (the)', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela (bolivarian republic of)', 'viet nam', 'virgin islands (british)', 'virgin islands (u.s.)', 'wallis and futuna', 'western sahara*', 'yemen', 'zambia', 'zimbabwe',
    "巴拿马", "所罗门群岛", "斯洛伐克", "贝宁", "圣多美和普林西比", "埃及", "中非", "冈比亚", "以色列", "科特迪瓦", "佛得角", "亚美尼亚", "波斯尼亚", "阿尔巴尼亚", "比利时", "马来西亚", "伊拉克", "苏里南", "津巴布韦", "伊朗", "布隆迪", "巴勒斯坦", "秘鲁", "立陶宛", "几内亚比绍", "智利", "新加坡", "卡塔尔", "利比亚", "萨摩亚", "墨西哥", "朝鲜", "缅甸", "柬埔寨", "英国", "巴西", "阿富汗", "日本", "格鲁吉亚", "巴基斯坦", "爱沙尼亚", "孟加拉", "毛里塔尼亚", "马尔代夫", "匈牙利", "沙特", "尼日尔", "拉脱维亚", "文莱", "哈萨克斯坦", "波兰", "安道尔", "卢森堡", "塞拉利昂", "阿曼", "台湾", "印度", "毛里求斯", "斯洛文尼亚", "韩国", "古巴", "希腊", "蒙古", "纳米比亚", "乍得", "摩纳哥", "埃塞俄比亚", "丹麦", "挪威", "哥伦比亚", "格林纳达", "摩洛哥", "德国", "斯里兰卡", "苏丹", "汤加", "澳大利亚", "新西兰", "叙利亚", "突尼斯", "刚果金", "阿根廷", "阿尔及利亚", "南非", "奥地利", "乌干达", "特立尼达和多巴哥", "喀麦隆", "塞舌尔", "葡萄牙", "保加利亚", "不丹", "东帝汶", "乌拉圭", "委内瑞拉", "瑞士", "玻利维亚", "西班牙", "摩尔多瓦", "加纳", "土库曼斯坦", "圭亚那", "吉尔吉斯", "坦桑尼亚", "尼日利亚", "塔吉克斯坦", "乌兹别克斯坦", "阿联酋", "马里", "瑞典", "白俄罗斯", "多哥", "法国", "罗马尼亚", "圣卢西亚", "俄罗斯", "赞比亚", "加蓬", "科威特", "卢旺达", "几内亚", "塞内加尔", "赤道几内亚", "泰国", "瑙鲁", "厄瓜多尔", "老挝", "荷兰", "马耳他", "越南", "尼泊尔", "博茨瓦纳", "利比里亚", "约旦", "多米尼克", "爱尔兰", "也门", "安哥拉", "吉布提", "巴林", "瓦努阿图", "土耳其", "美国", "刚果布", "塞浦路斯", "冰岛", "莱索托", "巴哈马", "意大利", "菲律宾", "索马里", "印尼", "阿塞拜疆", "肯尼亚", "巴巴多斯", "牙买加", "塞尔维亚", "列支敦士登", "密克罗尼西亚", "马其顿", "新几内亚", "黎巴嫩", "斐济", "莫桑比克", "厄立特里亚", "圣马力诺", "布基纳法索", "捷克", "芬兰", "科摩罗", "克罗地亚", "加拿大", "安提瓜和巴布达", "马达加斯加", "乌克兰", "图瓦卢", "圣文森特和格林纳丁斯", "多米尼加", "哥斯达黎加", "基里巴斯", "斯威士兰", "巴拉圭", "帕劳", "马拉维", "萨尔瓦多", "尼加拉瓜", "海地", "南苏丹", "伯利兹", "危地马拉", "洪都拉斯", "黑山共和国", "圣基茨和尼维斯","梵蒂冈", "马绍尔群岛",'中国']
    result = False
    name = name.lower()
    for country in _countries:
        if country==name:
            return True
    else:
        return result
   

def _dtypecheck(df,df_type):
    #通过field的dtype判断数据种类
    if df.dtype =='int64' and all(df[i]<df[i+1] for i in range(20)) and all(df<=df.shape[0]):
        # df_type["type"] = "ID"
        # df_type["subtype"] = 'id' 
        df_type["type"] = "categorical"
        df_type["subtype"] = 'id' 

        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))

    elif df.dropna().value_counts().index.isin([0, 1]).all() or len(df.dropna().value_counts().index)<=2:
        df_type["type"] = "categorical"
        df_type["subtype"] = 'boolean'
        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist())) 

    elif df.dtype == "datetime64[ns]":
        df_type["type"] = "temporal"
        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
        df_type["subtype"] = 'date'    
    elif df.dtype == "object":
        if _countries(df[0]):
            df_type["type"] = "geographical"
            df_type['subtype']='world'
            df_type['hierarchy']='country'
            df_type["values"] = df.fillna('unknown').unique().tolist()
        elif df[0] in [i.alpha_2 for i in list(pycountry.countries)] or df[0] in [i.alpha_3 for i in list(pycountry.countries)]:
            df_type["type"] = "geographical"
            df_type['subtype']='world'
            df_type['hierarchy']='country'
            df_type["values"] = df.fillna('unknown').unique().tolist()
        else: 
            try:
                df.apply(_moneyformatcheck)
                df_type["type"] = "numerical"
                df_type["measure"]=['sum','avg']
                df_type["mean"] = df.apply(_numericalreformat).mean()
                df_type["median"] = df.apply(_numericalreformat).median()
                df_type["std"] = df.apply(_numericalreformat).std()
                df_type["var"] = df.apply(_numericalreformat).var()
            except:
                try:
                    df.apply(_engcheck) 
                    df_type["type"] = "categorical"
                    df_type["subtype"] = df.name 
                    df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist())) 
                except:
                    try:
                        float(df[1])
                        df_type["type"] = "numerical"
                        df_type["measure"]=['sum','avg']
                        df_type["mean"] = df.apply(_numericalreformat).mean()
                        df_type["median"] = df.apply(_numericalreformat).median()
                        df_type["std"] = df.apply(_numericalreformat).std()
                        df_type["var"] = df.apply(_numericalreformat).var()
                    except:
                        df_type["type"] = "categorical"
                        df_type["subtype"] = df.name 
                        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist()))
    elif df.dtype =='int64' or df.dtype =='float64':
        df_type["measure"]=['sum','avg']
        if any(i in df.name.lower() for i in ['average','avg','mean']):
            df_type["measure"]=['sum','avg']
        elif any(i in df.name.lower() for i in ['total','sum','score', 'review', 'rating','length','stars','age','level','rate','percent','code','grade','mark','size','price','acceleration']):
            df_type["measure"]=['avg']
        elif any(i in df.name.lower() for i in ['min','max','high','low']):
            df_type["measure"]=['avg']
        df_type["type"] = "numerical"
        df_type["mean"] = df.mean()
        df_type["median"] = df.median()
        df_type["std"] = df.std()
        df_type["var"] = df.var()
    else:
        df_type["type"] = "categorical"
        df_type["subtype"] = df.name 
        df_type["values"] = list(map(lambda x: str(x),df.fillna('unknown').unique().tolist())) 

    return  df_type

def _moneyformatcheck(column):
    #数值是否包含单位符号 ¥ $
    if bool(re.search('[a-z]', column)):
        raise RuntimeError('testError') 
    else:
        c=float(sub(r'[^\d.]', '', column))
        return c

def _engcheck(column):
    #string处理
    if bool(re.search('[a-z]', column)):
        return column
    else:
        raise RuntimeError('testError') 

def _numericalreformat(column):
    #数值属性column中的string处理
    if type(column)==int:
        return column
    elif type(column)==str:
        try:
            return float(column.replace(',', ''))
        except:
            return 0
        # return float(cofloat(column.replace(',', '')))
        # try:
        #     return float(column)
        # except:
        #     try:
        #         float(column.replace(',', ''))
        #     except:
        #         raise RuntimeError
    elif type(column)==float:
        return column
  
  
def knn(W, x, k):
    # 添加的1e-9是为了数值稳定性
    cos = nd.dot(W, x.reshape((-1,))) / (                                    #reshape(-1) 广播，复制该表size，使其可以点乘   nd.dot()点乘     
        (nd.sum(W * W, axis=1) + 1e-9).sqrt() * nd.sum(x * x).sqrt())
    topk = nd.topk(cos, k=k, ret_typ='indices').asnumpy().astype('int32')    #nd.asnumpy() mxnet ->numpy
    return topk, [cos[i].asscalar() for i in topk]


