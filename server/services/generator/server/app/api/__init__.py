from flask import Blueprint
from flask_restful import Api
from .generate import Generate
from .fact import Fact
from .column2questions import Column2Questions

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

api.add_resource(Fact, '/fact')
api.add_resource(Generate, '/generate')
api.add_resource(Column2Questions, '/column2questions')

