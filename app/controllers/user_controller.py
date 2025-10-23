from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from app.config.logger import logger

class UserController:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def get_users(self):
        try:
            users = self.user_repository.get_all()
            logger.info("Controller: returned all users.")
            return users
        except Exception as e:
            logger.error(f"Controller error in get_users: {e}")
            raise

    def get_user(self, user_id: int):
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                logger.warning(f"Controller: user {user_id} not found.")
            return user
        except Exception as e:
            logger.error(f"Controller error in get_user({user_id}): {e}")
            raise

    def create_user(self, user_create: UserCreate):
        try:
            logger.info(f"Controller: creating user {user_create.email}")
            return self.user_repository.create(user_create)
        except Exception as e:
            logger.error(f"Controller error in create_user: {e}")
            raise

    def update_user(self, user_id: int, user_update: UserUpdate):
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                logger.warning(f"Controller: user {user_id} not found for update.")
                return None
            return self.user_repository.update(user, user_update)
        except Exception as e:
            logger.error(f"Controller error in update_user({user_id}): {e}")
            raise

    def delete_user(self, user_id: int):
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                logger.warning(f"Controller: user {user_id} not found for deletion.")
                return None
            return self.user_repository.delete(user)
        except Exception as e:
            logger.error(f"Controller error in delete_user({user_id}): {e}")
            raise
