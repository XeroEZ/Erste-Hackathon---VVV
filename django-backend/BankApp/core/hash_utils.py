from django.contrib.auth.hashers import make_password, check_password

def hash_password(raw_password: str) -> str:
    """Vytvorí hash hesla pomocou Argon2 (so saltom)."""
    return make_password(raw_password, hasher='argon2')

def verify_password(raw_password: str, hashed_password: str) -> bool:
    """Overí, či heslo zodpovedá hashovanému."""
    return check_password(raw_password, hashed_password)