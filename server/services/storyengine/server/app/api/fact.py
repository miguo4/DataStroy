from flask_restful import Resource, reqparse
import json
from ..algorithm2.data import load_df, load_schema
from ..algorithm2.fact import fact_scoring

class Fact(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file_name', required=True, help="file_name cannot be blank!")
        parser.add_argument('fact', required=True, help="fact cannot be blank!")
        parser.add_argument('method', required=True, help="method cannot be blank!")
        args = parser.parse_args()
        df = load_df('http://fileserver:6008/data/%s'%(args['file_name']))
        if df is None:
            return {
                'score': 0,
                'parameter': '',
                'possibility': 0,
                'information': 0,
                'significance': 0,
                'fact': {},
            }
        schema = load_schema(df)
        fact = json.loads(args['fact'])
        # print(fact)
        # method = args['method']
        method = 'sig'
        score, parameter, possibility, information, significance = fact_scoring(fact, df, schema, method)
        fact['score'] = score
        # print(fact['score'])
        fact['parameter'] = parameter
        return {
            'score': score,
            'parameter': parameter,
            'possibility': possibility,
            'information': information,
            'significance': significance,
            'fact': fact,
        }