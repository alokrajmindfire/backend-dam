from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.config.logger import logger
from fastapi import HTTPException, status
from app.config.hashing import Hasher

class UserRepository:
    """
    Repository class for performing CRUD operations on the User model.
    """
    def __init__(self, db: Session):
        """
        Initialize the UserRepository with a SQLAlchemy session.

        Args:
            db (Session): SQLAlchemy database session for performing queries.
        """
        self.db = db

    def get_all(self):
        """
        Retrieve all users from the database.

        Returns:
            list[User]: A list of all User objects stored in the database.

        Raises:
            Exception: If a database or query error occurs.
        """
        try:
            users = self.db.query(User).all()
            logger.info("Fetched all users from database.")
            return users
        except Exception as e:
            logger.exception(f"Error fetching users: {e}")
            raise

    def get_by_id(self, user_id: int):
        """
        Retrieve a single user by their ID.

        Args:
            user_id (int): The ID of the user to fetch.

        Returns:
            User | None: The User object if found, otherwise None.

        Raises:
            Exception: If a database error occurs during the query.
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.warning(f"User with id {user_id} not found.")
            return user
        except Exception as e:
            logger.exception(f"Error fetching user {user_id}: {e}")
            raise

    def create(self, user_create: UserCreate):
        """
        Create a new user in the database.

        Args:
            user_create (UserCreate): A Pydantic schema containing the user data (email, full_name, password, etc).

        Returns:
            User: The newly created User object.

        Raises:
            HTTPException: If a user with the given email already exists.
            Exception: If there’s an unexpected error during user creation.
        """
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
        """
        Update an existing user's details.

        Args:
            user (User): The existing User object to update.
            user_update (UserUpdate): A Pydantic model with updated user fields.

        Returns:
            User: The updated User object after committing changes.

        Raises:
            Exception: If a database error occurs during the update.
        """
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
        """
        Delete a user from the database.

        Args:
            user (User): The User object to delete.

        Returns:
            User: The deleted User object (for confirmation or logging).

        Raises:
            Exception: If a database error occurs during deletion.
        """
        try:
            self.db.delete(user)
            self.db.commit()
            logger.info(f"User deleted successfully: {user.id}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error deleting user {user.id}: {e}")
            raise
