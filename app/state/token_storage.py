from ..spotify import SpotifyClient
from ..exceptions import MissingRefreshTokenError, MissingTokenDataError, NoAuthenticatedUserError

class TokenStorage:
    _user_tokens = {}

    @classmethod
    def set_user_token_data(cls, access_token, refresh_token, expires_at):
        """Store or update tokens for current authenticated user"""
        user_id = cls.get_current_authenticated_user_id()
        if user_id is None:
            raise NoAuthenticatedUserError()
        
        if user_id not in cls._user_tokens:
            cls._user_tokens[user_id] = {}
        
        cls._user_tokens[user_id].update({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at
        })

    @classmethod
    def get_user_token_data(cls):
        """Retrieve the token data for currently authenticated user."""
        user_id = cls.get_current_authenticated_user_id()
        if user_id is None:
            raise NoAuthenticatedUserError()
        return cls._user_tokens.get(user_id, None)
    
    @classmethod
    def clear_user_token_data(cls):
        """Delete the token data for a specific user."""
        user_id = cls.get_current_authenticated_user_id()
        if user_id is None:
            raise NoAuthenticatedUserError()
        if user_id in cls._user_tokens:
            cls._user_tokens.pop(user_id)

    @classmethod
    def clear_all_tokens(cls):
        """Clear token data for all users."""
        cls._user_tokens.clear()

    @classmethod
    def refresh_access_token_data(cls):
        token_data = cls.get_user_token_data()

        if token_data is None:
            raise MissingTokenDataError()

        if 'refresh_token' not in token_data:
            raise MissingRefreshTokenError()

        new_token_data = SpotifyClient.oauth().refresh_access_token(token_data['refresh_token'])

        cls.set_user_token_data(
            access_token=new_token_data["access_token"],
            refresh_token=new_token_data["refresh_token"],
            expires_at=new_token_data["expires_at"]
        )

    def get_current_authenticated_user_id():
        from .auth import Auth
        return Auth.get_user_id()