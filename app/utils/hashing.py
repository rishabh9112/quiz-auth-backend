from passlib.context import CryptContext

pwd = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd.hash(password)

def verify_password(plain, hashed):
    return pwd.verify(plain, hashed)
