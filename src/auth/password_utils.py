from __future__ import annotations
import hashlib
import hmac
import secrets

def generate_salt() -> str:
    return secrets.token_hex(16)

def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120000).hex()

def create_password_hash(password: str) -> tuple[str, str]:
    salt = generate_salt()
    return hash_password(password, salt), salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    return hmac.compare_digest(hash_password(password, salt), stored_hash)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
