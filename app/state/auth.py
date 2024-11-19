import time
from flask import session

class Auth:
    
    @classmethod
    def set_user_id(cls, user_id):
        session["user_id"] = user_id

    @classmethod
    def get_user_id(cls):
        return session.get("user_id", None) 
    
    @classmethod
    def clear_user_id(cls):
        session.pop("user_id")

    @classmethod
    def get_status(cls):
        current_user_id = cls.get_user_id()
        if current_user_id is None:
            return "none"
        
        from .token_storage import TokenStorage
        current_user_token_data = TokenStorage.get_user_token_data()

        if current_user_token_data is None:
            return "none"
        
        current_time = int(time.time())
        expires_at = current_user_token_data['expires_at']
        if current_time >= expires_at:
            return "expired"
        
        return "valid"