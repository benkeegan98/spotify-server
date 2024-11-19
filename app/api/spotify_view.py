from flask import session, redirect, make_response, url_for, request
from flask.views import MethodView

from ..spotify import spotify_client
from ..state import TokenStorage, Auth
from ..exceptions import MissingRefreshTokenError, MissingTokenDataError, NoAuthenticatedUserError
from ..utils import TargetEndpoint


class SpotifyView(MethodView):
    def dispatch_request(self):
        """Dispatcher method that routes to specific methods based on endpoint."""
        match request.path:
            case "/spotify/current_track":
                return self.show_current_track()
            case "/spotify/save_current_track":
                return self.save_current_track()
            case _:
                return make_response("Endpoint not implemented", 404)
        
    def show_current_track(self):
        current_track = spotify_client.current_user_playing_track()
        return make_response(current_track)
    
    def save_current_track(self):
        match Auth.get_status():
            case "none":
                # Case 1: No accessToken, redirect to login
                TargetEndpoint.set(url_for('api.save_current_track'))
                return redirect(url_for('api.auth_login'))
            case "expired":
                # Case 2: accessToken is expired, refresh token
                try:
                    TokenStorage.refresh_access_token_data()
                except (MissingRefreshTokenError, MissingTokenDataError, NoAuthenticatedUserError):
                    # If no refresh token is available, redirect to login
                    TargetEndpoint.set(url_for('api.save_current_track'))
                    return redirect(url_for('api.auth_login'))
        
        # Case 3: authenticated
        return self._save_track_with_token()

    
    def _save_track_with_token(self):
        """Helper method to save the current track using a valid access token."""
        try:
            token_data = TokenStorage.get_user_token_data()
            if not token_data:
                raise MissingTokenDataError()
            
            spotify_client.auth = token_data['access_token']
            current_track_data = spotify_client.current_user_playing_track()

            if not current_track_data:
                return make_response("No track is currently playing.", 404)

            track_id = current_track_data["item"]["id"]
            spotify_client.current_user_saved_tracks_add([track_id])
            return make_response("Track saved successfully.", 200)
        
        except MissingTokenDataError:
            return make_response("Failed to save track. Missing token data", 500)

def register_endpoints(api):
    # Register the AuthView and map different URL rules to the `get` method with different endpoints
    api.add_url_rule('/spotify/current_track', view_func=SpotifyView.as_view('get_current_track'), methods=['GET'])
    api.add_url_rule('/spotify/save_current_track', view_func=SpotifyView.as_view('save_current_track'), methods=['GET'])