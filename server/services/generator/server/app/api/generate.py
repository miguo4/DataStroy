import os
import pandas as pd
import json
import requests
import random
import warnings
import logging
from flask_restful import Resource, reqparse
from ..algorithm import load_df, TalkGenerator, NL4DVGenerator
from flask import request
import requests
import traceback
import ast


def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok


class Generate(Resource):

    def __init__(self):
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                            level=logging.INFO, filename="calliope-lite.log", filemode="a")

    def post(self):

        warnings.filterwarnings("ignore")

        ip = request.remote_addr
        if request.headers.getlist("X-Real-IP"):
            ip = request.headers.getlist("X-Real-IP")[0]

        #
        # Parse request
        #
        parser = reqparse.RequestParser()
        parser.add_argument('file_name', required=True,
                            help="file_name cannot be blank!")
        parser.add_argument('question', required=True,
                            help="question cannot be blank!")
        parser.add_argument('model', default='calliope-talk',
                            help="select model(calliope-talk or nl4dv)")
        args = parser.parse_args()

        file_path = 'http://talk-fileserver:6028/data/%s' % (args['file_name'])
        schema_path = 'http://talk-fileserver:6028/data/%s.json' % (
            args['file_name'][:-4])
        # file_path = 'http://localhost:6028/data/%s'%(args['file_name'])
        # schema_path='http://localhost:6028/data/%s.json'%(args['file_name'][:-4])

        logging.info('[%s] starts insight extraction on [%s].' %
                     (ip, args['file_name']))

        if not exists(file_path):
            logging.error('[%s] Generation failed! Cannot find [%s].' %
                          (ip, args['file_name']))
            return {
                "error": "File does not exist"
            }

        if not exists(schema_path):
            logging.error('[%s] Generation failed! Cannot find [%s.json].' % (
                ip, args['file_name'][:-4]))
            return {
                "error": "schema does not exist"
            }

        #
        # Load file
        df = load_df(file_path)
        if df is None:
            logging.error(
                '[%s] Generation failed due to the data is not in UTF-8 / GBK.' % ip)
            return {
                'fail': 'Fail to decode data. Please upload utf-8 file.'
            }

        schema = requests.get(schema_path).json()

        if args['model'] == 'nl4dv':
            generator = NL4DVGenerator(schema, file_path)
            responsecode, responsecontent, responsestatus = generator.generate(args['question'])
            if responsestatus == "failed":
                return 'nl4dv errror'

            return responsecontent['visList']

        else:
            try:
                generator = TalkGenerator(schema,df)
                num_recursive_decompose = 3
                inputquestion = args['question'].replace("the", "").replace("?","").lower()
                responsecontent = generator.generate(inputquestion,num_recursive_decompose)
            except Exception as e:
                print(traceback.format_exc(),flush=True)
                print('talk-generator error', flush=True)
                responsecontent = "talk-generator error"
            
            return responsecontent
        
            # return {
            #     "story": [
            #         {
            #             "question" : 'show me the trend of user rating in 2010',
            #             "facts" : [
            #                 {
            #                     "type": "extreme",
            #                     "measure": [
            #                         {
            #                             "field": "Sales",
            #                         }
            #                     ],
            #                     "subspace": [],
            #                     "breakdown":[
            #                         {
            #                             "field": "Brand"
            #                         }
            #                     ],
            #                     "focus":[
            #                         {
            #                             "field": "Brand",
            #                             "value": "Toyota"
            #                         }
            #                     ],
            #                     "relavant_score": 0.9
            #                 },
            #                 {
            #                     "type": "trend",
            #                     "measure": [
            #                         {
            #                             "field": "Rating",
            #                         }
            #                     ],
            #                     "subspace": [],
            #                     "breakdown":[
            #                         {
            #                             "field": "Brand"
            #                         }
            #                     ],
            #                     "focus":[
            #                         {
            #                             "field": "Brand",
            #                             "value": "Toyota"
            #                         }
            #                     ],
            #                     "relavant_score": 0.7
            #                 }
            #             ]
            #         },
            #         {
            #             "question" : 'show me the trend of user rating in 2010',
            #             "facts" : [
            #                 {
            #                     "type": "extreme",
            #                     "measure": [
            #                         {
            #                             "field": "Sales",
            #                         }
            #                     ],
            #                     "subspace": [],
            #                     "breakdown":[
            #                         {
            #                             "field": "Brand"
            #                         }
            #                     ],
            #                     "focus":[
            #                         {
            #                             "field": "Brand",
            #                             "value": "Toyota"
            #                         }
            #                     ],
            #                     "relavant_score": 0.9
            #                 },
            #                 {
            #                     "type": "trend",
            #                     "measure": [
            #                         {
            #                             "field": "Rating",
            #                         }
            #                     ],
            #                     "subspace": [],
            #                     "breakdown":[
            #                         {
            #                             "field": "Brand"
            #                         }
            #                     ],
            #                     "focus":[
            #                         {
            #                             "field": "Brand",
            #                             "value": "Toyota"
            #                         }
            #                     ],
            #                     "relavant_score": 0.7
            #                 }
            #             ]
            #         }
            #     ]
            # }