import os
import pandas as pd
import json
import jsonpickle
import requests
import random
import warnings
from flask_restful import Resource, reqparse
from ..algorithm2 import load_schema, load_df, RandomGenerator, FactFactory

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

class GenerateRamdom(Resource):
    def post(self):
        warnings.filterwarnings("ignore")
        #
        # Parse request
        #
        parser = reqparse.RequestParser()
        parser.add_argument('file_name', required=True, help="file_name cannot be blank!")
        parser.add_argument('max_story_length', required=True, help="max_story_length cannot be blank!")
        args = parser.parse_args()
        file_path = 'http://fileserver:6008/data/%s'%(args['file_name'])
        if not exists(file_path):
            return {
                "error": "File not exist"
            }

        #
        # Load file
        #
        df = load_df(file_path)
        if df is None:
            return {
                'fail': 'Fail to decode data. Please upload utf-8 file.'
            }
        schema = load_schema(df)
        if schema['statistics']['column'] < 2:
            return {
                'fail': 'We need at least two data columns to generate visual content.'
            }
        if schema['statistics']['numerical'] < 1:
            return {
                'fail': 'We need at least one numerical column to generate visual content.'
            }
        if schema['statistics']['categorical'] + schema['statistics']['geographical'] + schema['statistics']['temporal'] < 1:
            return {
                'fail': 'We need at least one categorical/temporal/geographical column to generate visual content.'
            }

        #
        # Generator
        #
        generator = RandomGenerator(df, schema)

        candidates = generator.generate()
        candidates = list(candidates)
        max_story_length = int(args['max_story_length'])
        if len(candidates) > max_story_length:
            candidates = random.sample(candidates, max_story_length)
            for candidate in candidates:
                if isinstance(candidate["parameter"], float):
                    candidate["parameter"] = round(candidate["parameter"], 2)
        
        return {
            "story": {
                "facts": candidates
            }
        }
