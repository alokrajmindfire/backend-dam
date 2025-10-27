from app.config.logger import logger
import bcrypt

class Hasher:
    """
    Handles hashing and verifying passwords using bcrypt and SHA-256 for extra security.
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify that a plain text password matches its hashed version.
        """
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.exception(f"Error verifying password: {e}")
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password securely using SHA-256 + bcrypt.
        """
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return hashed_password.decode('utf-8')
        except Exception as e:
            logger.exception(f"Error hashing password: {e}")
            raise