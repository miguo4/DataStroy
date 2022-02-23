from flask import Blueprint
from flask_restful import Api
from .upload import Upload
from .share import Share

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

api.add_resource(Upload, '/upload')
api.add_resource(Share, '/share')
