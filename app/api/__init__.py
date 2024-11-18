from flask import Blueprint
from .auth_view import register_endpoints as register_auth_endpoints
from .spotify_view import register_endpoints as register_spotify_endpoints

api = Blueprint('api', __name__)

register_auth_endpoints(api)
register_spotify_endpoints(api)