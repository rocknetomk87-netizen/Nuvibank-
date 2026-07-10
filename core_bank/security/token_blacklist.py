blacklisted_tokens = set()

def add_token_to_blacklist(jti):
    blacklisted_tokens.add(jti)

def is_token_revoked(jti):
    return jti in blacklisted_tokens
