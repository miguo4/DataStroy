import werkzeug, os, json
import logging
from flask_restful import Resource, reqparse
from ..flask_uploads import UploadSet, DATA
from ..preprocessing import DataFormat, Processor,load_df
from ..preprocessing.Operators import CreateHierarchyOpt, RemoveBlankOpt, LabelTypeOpt,TemGeoNormalizationOpt,NormalizationOpt,toSchemaOpt,StatisticsOpt
from flask import request

upload = UploadSet('csvs', DATA)
ALLOWED_EXTENSIONS = set(['csv'])

class Upload(Resource):

    def __init__(self):
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO, filename="calliope-lite.log", filemode="a")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args['file']
        file.filename=file.filename.replace(' ','_')
        ip = request.remote_addr
        if request.headers.getlist("X-Real-IP"):
            ip = request.headers.getlist("X-Real-IP")[0]

        if file and self.allowed_file(file.filename):

            logging.info('[%s] requests to upload [%s].'%(ip,file.filename))
            
            upload.save(file, overwrite=True)

            df = load_df('./csvs/%s'%(file.filename))

            if df is None:
                logging.error('[%s] [%s] is not in UTF-8 / GBK or not sperated by , or ;'%(ip,file.filename))
                return {
                    'status':'error',
                    'message_en':'File parsing error. The columns should be separated by , or ; and the file should be encoded in UTF-8 or GBK.',
                    'message_zh':'文件解析有误，本系统仅支持 UTF-8 / GBK 编码下用 , 或 ; 分割的csv文件。'
                }
                
            df=df.dropna().reset_index(drop=True)
            if df.empty:
                logging.error('[%s] [%s] contains too many empty fileds.'%(ip,file.filename))
                return {
                    'status':'error',
                    'message_en':'The input file contains too many empty fields, which cannot be visualized. Please try again after cleaning your data.',
                    'message_zh':'输入数据包含过多空白项，无法进行数据洞察。请检查并清理数据后重新上传。'
                }            

            if df.columns.str.contains('Unnamed').sum()> df.shape[1]/2:
                logging.error('[%s] [%s] has a no-hearder column.'%(ip,file.filename))
                return {
                    'status':'error',
                    'message_en':'The file contains empty column headers. Please try again after cleaning your data.',
                    'message_zh':'输入数据包含空白表头，无法进行数据洞察。请检查并清理数据后重新上传。'
                }

            # if df.shape[0]>=2000:
            #     return {
            #         'status':'error',
            #         'message_en':'Sorry, we currently do not support the file that exceeds 2000 rows.',
            #         'message_zh':'抱歉，目前版本不支持大于2000行数据。'
            #     }
            # if 'name' in df.columns:
            #     df.columns = ['namee' if x=='name' else x for x in df.columns]                
            
            df.columns = [x.lower() for x in df.columns]
            data = DataFormat(df)
            #create a processor for the loaded data
            pro = Processor(data = data)
            for colname in data.data["df"].columns:
                pro.add(LabelTypeOpt(data = data, colname=colname))
                pro.add(RemoveBlankOpt(data = data, colname=colname))
                pro.add(NormalizationOpt(data = data, colname=colname))
            pro.add(StatisticsOpt(data = data))
            pro.add(CreateHierarchyOpt(data = data))
            pro.add(TemGeoNormalizationOpt(data = data))
            pro.add(toSchemaOpt(data = data))
            result = pro.run()
            schema=result.data['schema']
            if schema['statistics']['numerical'] < 1: 
                logging.error('[%s] [%s] has less than one numerical column.'%(ip,file.filename))
                return {
                    'status':'error',
                    'message_en':'Calliope needs at least one numerical column to generate visual content.',
                    'message_zh':'数据中需要至少包含一列数值属性方可生进行有效的数据洞察。'
                }
            if schema['statistics']['geographical']+schema['statistics']['categorical']+schema['statistics']['temporal'] < 1 :
                logging.error('[%s] [%s] has less than one geographical/categorical/temporal column.'%(ip,file.filename))
                return {
                    'status':'error',
                    'message_en':'We need at least one geographical/categorical/temporal column to generate visual content.',
                    'message_zh':'数据中需要至少包含至少一列 地理 或 类别 或 时间 属性方可进行有效的数据洞察。'
                }

            logging.info('[%s] sucessfully uploaded and preprocessed the file [%s] in Calliope.'%(ip,file.filename))

            result.data['df'].to_csv('./csvs/%s'%(file.filename),index=False)
            with open('./csvs/%s.json'%(file.filename[:-4]),'w') as f:
                json.dump(schema, f)
            return {
                "file_name": file.filename,
                "file_url": "/data/%s"%(file.filename),
                "schema": schema
            }
        else:
            logging.error('[%s] cannot find the file.'%ip)
            return {
                'message_en':'Cannot find the file',
                'message_zh':'无法找到相关文件',
                'message': 'Cannot find the file',
                'status':'error'
            }

    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    

