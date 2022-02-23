import os
import pandas as pd
import json
import jsonpickle
import requests
import warnings
from flask_restful import Resource, reqparse
from ..algorithm2 import load_schema, load_df, Generator, FactFactory, Tree, Node

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

class GenerateV3(Resource):
    def post(self):
        warnings.filterwarnings("ignore")
        #
        # Parse request
        #
        parser = reqparse.RequestParser()
        parser.add_argument('file_name', required=True, help="file_name cannot be blank!")
        parser.add_argument('max_story_length', required=True, help="max_story_length cannot be blank!")
        parser.add_argument('time_limit', required=True, help="time_limit cannot be blank!")
        parser.add_argument('reward_weight', required=True, help="reward_weight cannot be blank!")
        parser.add_argument('method', required=True, help="method cannot be blank!")
        parser.add_argument('tree', required=True, help="tree cannot be blank!")
        args = parser.parse_args()
        file_path = 'http://fileserver:6008/data/%s'%(args['file_name'])
        if not exists(file_path):
            return {
                "error": "File not exist"
            }
        
        #
        # Goal
        #
        max_story_length = int(args['max_story_length'])
        time_limit = int(args['time_limit'])
        goal = {
            "limit": time_limit,
            "length": max_story_length,
            "info": 50
        }
        
        #
        # Reward
        #
        reward_weight = args['reward_weight']
        weight = json.loads(reward_weight)
        reward = weight

        #
        # Fact Factory
        #
        df = load_df(file_path)
        if df is None:
            return {
                'fail': 'Fail to decode data. Please upload utf-8 file.'
            }
        schema = load_schema(df)
        if schema['statistics']['column'] <= 2:
            return {
                'fail': 'It needs more data columns to generate a story automatically.'
            }
        if schema['statistics']['categorical'] + schema['statistics']['geographical'] + schema['statistics']['temporal'] < 2:
            return {
                'fail': 'It needs more categorical/temporal/geographical columns to generate a story automatically.'
            }
        method = args['method']
        factory = FactFactory(df, schema, method)

        #
        # Tree
        #
        if args['tree'] == "":
            tree = None
        else:
            tree = jsonpickle.decode(args['tree'])

        #
        # Generator
        #
        generator = Generator(df, schema, goal, reward, factory, tree)

        story, newtree = generator.generateIteratively()
        
        return {
            "tree": newtree,
            "story": story,
        }
