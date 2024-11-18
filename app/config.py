import os
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

class Config:
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
    SESSION_COOKIE_NAME = 'spotify_auth_session'
    SECRET_KEY = secrets.token_hex(32)
