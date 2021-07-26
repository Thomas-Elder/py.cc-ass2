
from .dynamodb import get_user, get_users

def check_password(email: str, password: str) -> bool:
    """
    check_password

    Returns true if the password stored with the email matches.
    """
    user = get_user(email=email)
    
    if user is None:
        return False
    else:
        return user['info']['password'] == password

def check_email_unique(email: str) -> bool:
    """
    check_email_unique
    
    Returns true if the given email is not already in the database.
    """
    user = get_user(email)

    return not user is None