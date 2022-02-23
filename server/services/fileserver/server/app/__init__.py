from flask import Flask
from flask_cors import CORS
from config import Config
from .api import api_blueprint
from .flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class

def create_app():
    app = Flask(__name__, instance_relative_config=True,static_url_path='/data', static_folder='../csvs')
    CORS(app)
    app.config.from_object(Config)
    csvs = UploadSet('csvs', DATA)
    configure_uploads(app, csvs)
    patch_request_class(app, None)
    app.register_blueprint(api_blueprint, url_prefix = '')
    return app