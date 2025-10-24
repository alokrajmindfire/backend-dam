import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        print("pass",password)
        sha256_hash = hashlib.sha256(password.encode()).hexdigest()
        # Hash the SHA-256 hash using bcrypt
        return pwd_context.hash(sha256_hash)