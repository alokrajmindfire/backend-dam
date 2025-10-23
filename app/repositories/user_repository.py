from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.config.logger import logger
from fastapi import HTTPException, status

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        try:
            users = self.db.query(User).all()
            logger.info("Fetched all users from database.")
            return users
        except Exception as e:
            logger.exception(f"Error fetching users: {e}")
            raise

    def get_by_id(self, user_id: int):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.warning(f"User with id {user_id} not found.")
            return user
        except Exception as e:
            logger.exception(f"Error fetching user {user_id}: {e}")
            raise

    def create(self, user_create: UserCreate):
        try:
            existing_user = self.db.query(User).filter(User.email == user_create.email).first()
            if existing_user:
                logger.info(f"User already exists with email: {user_create.email}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User already exists with email: {user_create.email}"
                )
            user = User(
                email=user_create.email,
                full_name=user_create.full_name,
                password=user_create.password
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User created successfully: {user.email}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error creating user {user_create.email}: {e}")
            raise

    def update(self, user: User, user_update: UserUpdate):
        try:
            for key, value in user_update.dict().items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User updated successfully: {user.id}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error updating user {user.id}: {e}")
            raise

    def delete(self, user: User):
        try:
            self.db.delete(user)
            self.db.commit()
            logger.info(f"User deleted successfully: {user.id}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error deleting user {user.id}: {e}")
            raise
