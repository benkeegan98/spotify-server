from flask import session, redirect, make_response, url_for, request
from flask.views import MethodView

from ..spotify import spotify_client
from ..state import TokenStorage, AuthState
from ..exceptions import MissingRefreshTokenError, MissingTokenDataError
from ..utils import get_user_id_from_session, set_target_endpoint


class SpotifyView(MethodView):
    def dispatch_request(self):
        """Dispatcher method that routes to specific methods based on endpoint."""
        print(request.path)
        if request.path == "/spotify/current_track":
            return self.show_current_track()
        elif request.path == "/spotify/save_current_track":
            return self.save_current_track()
        else:
            return make_response("Endpoint not implemented", 404)
        
    def show_current_track(self):
        current_track = spotify_client.current_user_playing_track()
        return make_response(current_track)
    
    def save_current_track(self):

        user_id = self.get_user_id()
        auth_status = AuthState.get_auth_status(user_id)

        if auth_status == "none":
            # Case 1: No accessToken, redirect to login
            set_target_endpoint(url_for('api.save_current_track'))
            return redirect(url_for('api.auth_login'))
        
        elif auth_status == "expired":
            # Case 2: accessToken is expired, refresh token
            try:
                TokenStorage.refresh_access_token_data()
            except (MissingRefreshTokenError, MissingTokenDataError) as e:
                # If no refresh token is available, redirect to login
                set_target_endpoint(url_for('api.save_current_track'))
                return redirect(url_for('api.auth_login'))
            
        return self._save_track_with_token()
    
    def _save_track_with_token(self):
        """Helper method to save the current track using a valid access token."""
        try:
            user_id = get_user_id_from_session()
            token_data = TokenStorage.get_user_token_data(user_id)
            if not user_id or not token_data:
                raise Exception()
            
            spotify_client.auth = token_data['access_token']
            current_track_data = spotify_client.current_user_playing_track()

            if not current_track_data:
                return make_response("No track is currently playing.", 404)

            track_id = current_track_data["item"]["id"]
            spotify_client.current_user_saved_tracks_add([track_id])
            return make_response("Track saved successfully.", 200)
        
        except Exception as e:
            print(f"Failed to save track: {e}")
            return make_response("Failed to save track.", 500)

def register_endpoints(api):
    # Register the AuthView and map different URL rules to the `get` method with different endpoints
    api.add_url_rule('/spotify/current_track', view_func=SpotifyView.as_view('get_current_track'), methods=['GET'])
    api.add_url_rule('/spotify/save_current_track', view_func=SpotifyView.as_view('save_current_track'), methods=['GET'])