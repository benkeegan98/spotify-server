import time

class AuthState:

    _user_states = {}
    
    @classmethod
    def set_current_authenticated_user_id(cls, user_id):
        # Initialize state for this user if it doesn't exist
        if user_id not in cls._user_states:
            cls._user_states[user_id] = {"current_authenticated_user_id": None}
        cls._user_states[user_id]["current_authenticated_user_id"] = user_id

    @classmethod
    def get_current_authenticated_user_id(cls, user_id):
        user_state = cls._user_states.get(user_id)
        return user_state.get("current_authenticated_user_id", None) if user_state else None
    
    @classmethod
    def clear_auth_state(cls, user_id):
        if user_id in cls._user_states:
            cls._user_states[user_id] = {"current_authenticated_user_id": None}

    @classmethod
    def get_auth_status(cls, user_id):
        current_user_id = cls.get_current_authenticated_user_id(user_id)

        if current_user_id is None:
            return "none"
        
        from .token_storage import TokenStorage
        current_user_token_data = TokenStorage.get_user_token_data(user_id)

        if current_user_token_data is None:
            return "none"
        
        current_time = int(time.time())
        expires_at = current_user_token_data['expires_at']
        if current_time >= expires_at:
            return "expired"
        
        return "valid"