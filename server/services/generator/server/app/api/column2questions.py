from flask_restful import Resource, reqparse
import json
import requests
from ..algorithm.column2questions import BottomupQuestionGenerator
from ..algorithm.column2questions import TopdownQuestionGenerator
from ..algorithm.column2questions import SimpleQuestionGenerator
from ..algorithm import load_df
import random

class Column2Questions(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file_name', required=True, help="file_name cannot be blank!")
        parser.add_argument('column_name', required=True, help="column_name cannot be blank!")
        args = parser.parse_args()

        # df = load_df('http://localhost:6028/data/%s'%(args['file_name']))
        # schema_path='http://localhost:6028/data/%s.json'%(args['file_name'][:-4])

        df = load_df('http://talk-fileserver:6028/data/%s'%(args['file_name']))
        schema_path='http://talk-fileserver:6028/data/%s.json'%(args['file_name'][:-4])
        schema=requests.get(schema_path).json()
        
        cg_topdown = TopdownQuestionGenerator()
        cg_topdown.load(schema)
        topdown_question_json=cg_topdown.generate()
        tdlist = list(filter(lambda x: x['question'].lower().count(args['column_name'].lower()) == 1, topdown_question_json))
        


        return random.sample(list(map(lambda x: x['question'], tdlist)), min(len(tdlist),5))
    















