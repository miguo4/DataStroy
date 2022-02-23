from flask import Blueprint
from flask_restful import Api
from .generate2 import GenerateV2
from .generate3 import GenerateV3
from .generateRandom import GenerateRamdom
from .fact import Fact

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

api.add_resource(Fact, '/fact')
api.add_resource(GenerateV2, '/generate-v2')
api.add_resource(GenerateV3, '/generate-v3')
api.add_resource(GenerateRamdom, '/generate-random')
