import werkzeug, os, json
import uuid
from flask_restful import Resource, reqparse
import json
from ..flask_uploads import UploadSet, DATA
from flask import request

upload = UploadSet('csvs', DATA)

class Share(Resource):

    # get from BASE_URL/data/share/xxxx.json

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('share_json', required=True, help="share_json cannot be blank!")
        args = parser.parse_args()
        share_json = args['share_json']
        filename = uuid.uuid4().hex
        if not os.path.isdir('./csvs/share'):
            os.mkdir('./csvs/share')
        jsonFile = open('./csvs/share/%s.json'%(filename), 'w')
        jsonFile.write(share_json)
        jsonFile.close()
        return {
            'share_id':filename
        }

    