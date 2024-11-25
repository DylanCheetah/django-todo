# Exception Classes
# =================
class UserBanned(Exception):
    """
    Exception raised when a banned user attempts to access something they
    shouldn't have access to.
    """


class InvalidTokenScope(Exception):
    """
    Exception raised when a token has the incorrect scope for the desired
    action.
    """
