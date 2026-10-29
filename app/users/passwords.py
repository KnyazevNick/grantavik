from pwdlib import PasswordHash



hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """return hash of the input password"""
    return hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """check password with the hash, return bool"""
    return hasher.verify(password, password_hash)