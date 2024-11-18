from flask import session
from ..spotify import sp_oauth
from ..exceptions import MissingRefreshTokenError, MissingTokenDataError, NoAuthenticatedUserError

class TokenStorage:
    _user_tokens = {}

    @classmethod
    def set_user_token_data(cls, user_id, access_token, refresh_token, expires_at):
        """Store or update tokens for current authenticated user"""
        if user_id not in cls._user_tokens:
            cls._user_tokens[user_id] = {}

        user_id = cls.get_current_authenticated_user_id(user_id)
        if user_id is None:
            raise NoAuthenticatedUserError()
        
        cls._user_tokens[user_id].update({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at
        })

    @classmethod
    def get_user_token_data(cls, user_id):
        """Retrieve the token data for currently authenticated user."""
        return cls._user_tokens.get(user_id, None)
    
    @classmethod
    def delete_user_token_data(cls, user_id):
        """Delete the token data for a specific user."""
        if user_id in cls._user_tokens:
            cls._user_tokens.pop(user_id)

    @classmethod
    def clear_all_tokens(cls):
        """Clear token data for all users."""
        cls._state.clear()

    @classmethod
    def refresh_access_token_data(cls, user_id):
        token_data = cls.get_user_token_data(user_id)

        if token_data is None:
            raise MissingTokenDataError()

        if 'refresh_token' not in token_data:
            raise MissingRefreshTokenError()

        new_token_data = sp_oauth.refresh_access_token(token_data['refresh_token'])

        cls.set_user_token_data(
            user_id,
            access_token=new_token_data["access_token"],
            refresh_token=new_token_data["refresh_token"],
            expires_at=new_token_data["expires_at"]
        )

    def get_current_authenticated_user_id(user_id):
        from .auth_state import AuthState
        return AuthState.get_current_authenticated_user_id(user_id)