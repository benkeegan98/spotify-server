import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ..config import Config



spotify_client = spotipy.Spotify(auth_manager=sp_oauth)

class SpotifyClient:
    
    @classmethod
    def get(self):
        oauth = self.oauth()
        return spotipy.Spotify(auth_manager=oauth)

    @classmethod
    def oauth(self):
        return SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope='user-library-read user-read-playback-state user-read-currently-playing playlist-modify-private playlist-modify-public user-library-modify'
        )
