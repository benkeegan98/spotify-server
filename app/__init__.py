from flask import Flask

from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure "/<path>" = "/<path>/", and no redirection happens
    app.url_map.strict_slashes = False
    app.url_map.merge_slashes = False

    with app.app_context():

        from .api import api
        app.register_blueprint(api)

        return app


