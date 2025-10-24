from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config.dbconf import SessionLocal
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    controller = UserController(db)
    return controller.get_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    controller = UserController(db)
    user = controller.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    controller = UserController(db)
    return controller.create_user(user_create)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    controller = UserController(db)
    user = controller.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    controller = UserController(db)
    user = controller.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
