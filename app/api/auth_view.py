from flask import session, redirect, make_response, url_for, request
from flask.views import MethodView

from ..spotify import sp_oauth, spotify_client
from ..state import TokenStorage, AuthState 
from ..exceptions import MissingRefreshTokenError, MissingTokenDataError


class AuthView(MethodView):
    def dispatch_request(self):
        """Dispatcher method that routes to specific methods based on endpoint."""
        if request.path == "/auth/success":
            return self.success()
        elif request.path == "/auth/redirect":
            return self.redirect_callback()
        else:
            return self.login()
        

    def login(self):
        """Login route."""
        user_id = self.get_user_id()
        auth_status = AuthState.get_auth_status(user_id)
        if auth_status == "none":
            return redirect(sp_oauth.get_authorize_url())
        if auth_status == "expired":
            try:
                TokenStorage.refresh_access_token_data()
            except (MissingRefreshTokenError, MissingTokenDataError):
                return redirect(sp_oauth.get_authorize_url())
            
        return self.success()

    def success(self):
        """Success route."""
        return make_response("Auth was successful")

    def redirect_callback(self):
        """Callback route for Spotify authentication."""
        code = request.args.get('code')
        if code:
            user = spotify_client.me()
            user_id = user["id"]
            AuthState.set_current_authenticated_user_id(user_id)
            session["user_id"] = user_id

            token_data = sp_oauth.get_access_token(code, as_dict=True)
            TokenStorage.set_user_token_data(
                user_id,
                access_token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                expires_at=token_data["expires_at"]
            )
            
            user_token_data = TokenStorage.get_user_token_data(user_id)
            if user_token_data:
                # Check if there's a target endpoint stored and redirect there
                target_endpoint = session.pop('target_endpoint', None)
                if target_endpoint:
                    return redirect(target_endpoint)
                return redirect(url_for('api.auth_success'))
            else:
                return make_response("Failed to retrieve tokens.", 400)
        else:
            return make_response("Authorization failed.", 400)
        
    def get_user_id(self):
        # Extract user ID from the session
        return session.get("user_id") or None


def register_endpoints(api):
    # Register the AuthView and map different URL rules to the `get` method with different endpoints
    api.add_url_rule('/auth/login', view_func=AuthView.as_view('auth_login'), methods=['GET'])
    api.add_url_rule('/auth/success', view_func=AuthView.as_view('auth_success'), methods=['GET'])
    api.add_url_rule('/auth/redirect', view_func=AuthView.as_view('auth_redirect'), methods=['GET'])
