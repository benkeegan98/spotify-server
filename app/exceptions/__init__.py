class MissingRefreshTokenError(Exception):
    """Custom exception for token refresh errors."""
    pass

class MissingTokenDataError(Exception):
    """Custom exception for when token is missing."""
    pass

class NoAuthenticatedUserError(Exception):
    """Custom exception for when no user is authenticated."""
    pass

__all__ = ["MissingRefreshTokenError", "MissingTokenDataError"]