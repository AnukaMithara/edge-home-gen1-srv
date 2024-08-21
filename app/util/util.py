import base64

from cryptography.fernet import Fernet

from app.config.config import ENCRYPT_KEY


def encrypt_password(password):
    f = Fernet(base64.urlsafe_b64encode(ENCRYPT_KEY))
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password


# Decrypt a password
def decrypt_password(encrypted_password):
    f = Fernet(base64.urlsafe_b64encode(ENCRYPT_KEY))
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password
