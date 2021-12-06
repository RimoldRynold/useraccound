from secrets import token_urlsafe
def get_token():
    return token_urlsafe(24)