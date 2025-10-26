import bcrypt
from cryptography.fernet import Fernet

# Load key from file (generate once)
with open("Utils/key.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def encrypt(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()