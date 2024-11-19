import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ..config import Config

class SpotifyClient:
    
    @classmethod
    def get(self):
        return spotipy.Spotify(auth_manager=self.oauth())

    @classmethod
    def oauth(self):
        return SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope='user-library-read user-read-playback-state user-read-currently-playing playlist-modify-private playlist-modify-public user-library-modify'
        )
