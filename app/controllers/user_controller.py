from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate

class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self):
        return self.db.query(User).all()

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_create: UserCreate):
        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            password=user_create.password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user_update: UserUpdate):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in user_update.dict().items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user
