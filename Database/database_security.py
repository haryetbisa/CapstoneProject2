import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def load_or_create_key():
    """Loads the encryption key or generates one if it doesn't exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

fernet = Fernet(load_or_create_key())

def encrypt_data(plaintext: str) -> str:
    """Encrypts a plaintext string into a secure token string."""
    if not plaintext:
        return ""
    return fernet.encrypt(str(plaintext).encode("utf-8")).decode("utf-8")

def decrypt_data(token: str) -> str:
    """Decrypts an encrypted token back into plaintext."""
    if not token:
        return ""
    try:
        return fernet.decrypt(token.encode("utf-8")).decode("utf-8")
    except Exception:
        return token