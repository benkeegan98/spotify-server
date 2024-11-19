from flask import session

def set_user_id_in_session(user_id):
    session["user_id"] = user_id

def get_user_id_from_session():
    # Extract user ID from the session
    return session.get("user_id") or None

def set_target_endpoint(url):
    session["target_endpoint"] = url

def get_target_endpoint():
    return session.pop('target_endpoint', None)
