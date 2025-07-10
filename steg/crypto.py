from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def _derive_key(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_message(message: str, password: str) -> str:
    """Encrypt a message using AES encryption."""
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    fernet = Fernet(key)
    
    encrypted_data = fernet.encrypt(message.encode())
    # Prepend salt to encrypted data
    return base64.b64encode(salt + encrypted_data).decode()

def decrypt_message(encrypted_message: str, password: str) -> str:
    """Decrypt a message using AES decryption."""
    try:
        encrypted_data = base64.b64decode(encrypted_message.encode())
        salt = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        key = _derive_key(password, salt)
        fernet = Fernet(key)
        
        decrypted_data = fernet.decrypt(ciphertext)
        return decrypted_data.decode()
    except Exception:
        raise ValueError("Decryption failed - incorrect password or corrupted data")