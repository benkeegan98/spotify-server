INSTRUCTIONS

CREATE FOLDER

CREATE VENV
 - Check python version -- python -V
 - python -m venv venv
 - source venv/bin/activate

PIP INSTALL FLASK
 - pip install Flask

CREATE APP FOLDER
 - __init__.py
    from flask import Flask

    def create_app():
        app = Flask(__name__)

        # OPTIONAL - ensure "/<path>" = "/<path>/", so no redirection happens
        app.url_map.strict_slashes = False
        app.url_map.merge_slashes = False

        with app.app_context():
            
            # register api blueprint here
            from .api import api
            app.register_blueprint(api)

            return app

CREATE wsgi.py as entry point
 - wsgi.py
    from app import create_app

    app = create_app()

    if __name__ == "__main__":
        app.run(host='0.0.0.0')

INSIDE APP, CREATE api.py
 - Can split this up into modules if we want but for purposes of this, will write api in one file
 - api.py:
    from flask import Blueprint, request, make_response, jsonify
    from flask.views import MethodView

    api = Blueprint('api', __name__)

    either MethodViews:

        class MainAPI(MethodView):

            def get(self, param):
                ...
        
        main_view = MainAPI.as_view('main_api')
        api.add_url_rule('/main/', view_func=main_view, defaults={'param': None}, methods=['GET'])
    
    or define routes:

        @api.route('/main/'):
        def func(param=None):
            ...
    

access endpoint with:
    request.endpoint

access url args:
    request.args

access json post body:
    request.json