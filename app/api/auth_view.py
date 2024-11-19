from flask import redirect, make_response, url_for, request
from flask.views import MethodView
import logging

from ..spotify import SpotifyClient
from ..state import TokenStorage, Auth
from ..exceptions import MissingRefreshTokenError, MissingTokenDataError, NoAuthenticatedUserError
from ..utils import TargetEndpoint

logging.basicConfig(level=logging.INFO)

class AuthView(MethodView):
    def dispatch_request(self):
        """Dispatcher method that routes to specific methods based on endpoint."""
        match request.path:
            case "/auth/success":
                return self.success()
            case "/auth/redirect":
                return self.redirect_callback()
            case _:
                return self.login()  

    def login(self):
        """Login route."""
        match Auth.get_status():
            case "none":
                return redirect(SpotifyClient.oauth().get_authorize_url())
            case "expired":
                try:
                    TokenStorage.refresh_access_token_data()
                except (MissingRefreshTokenError, MissingTokenDataError, NoAuthenticatedUserError):
                    return redirect(SpotifyClient.oauth().get_authorize_url())
            
        return self.success()

    def success(self):
        """Success route."""
        return make_response("Auth was successful")

    def redirect_callback(self):
        """Callback route for Spotify authentication."""
        code = request.args.get('code')
        if not code:
            return make_response("Authorization failed.", 400)
        
        logging.info(f"Authorization code received: {code}")
        
        user = SpotifyClient.get().me()
        Auth.set_user_id(user["id"])

        logging.info(f"Set user id in session: {user["id"]}")

        token_data = SpotifyClient.oauth().get_access_token(code, as_dict=True)
        logging.info(f"Token data: {token_data}")

        TokenStorage.set_user_token_data(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            expires_at=token_data["expires_at"]
        )
        
        user_token_data = TokenStorage.get_user_token_data()
        logging.info(f"Retrieved token data: {user_token_data}")
        if not user_token_data:
            return make_response("Failed to retrieve tokens from TokenStorage.", 400)

        # Check if there's a target endpoint stored and redirect there
        if TargetEndpoint.present():
            logging.info(f"Redirecting to target endpoint")
            return TargetEndpoint.redirect()
        return redirect(url_for('api.auth_success'))
            
            


def register_endpoints(api):
    # Register the AuthView and map different URL rules to the `get` method with different endpoints
    api.add_url_rule('/auth/login', view_func=AuthView.as_view('auth_login'), methods=['GET'])
    api.add_url_rule('/auth/success', view_func=AuthView.as_view('auth_success'), methods=['GET'])
    api.add_url_rule('/auth/redirect', view_func=AuthView.as_view('auth_redirect'), methods=['GET'])
