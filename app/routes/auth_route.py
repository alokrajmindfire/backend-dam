from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.config.dbconf import SessionLocal
from app.controllers.auth_controller import authenticate_user, create_access_token
from app.schemas.auth_schema import Token, LoginSchema
from app.config.config import settings
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.controllers.user_controller import UserController

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=Token)
def login(response: Response, payload: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.email)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user record in the database.

    Args:
        user_create (UserCreate): Schema containing user creation data (e.g., email, password).
        db (Session): Database session provided by the dependency injection system.

    Returns:
        UserResponse: The newly created user's details.
    """
    controller = UserController(db)
    return controller.create_user(user_create)

@router.post("/logout")
def logout(response: Response):
    """
    Log out the user by deleting the JWT cookie.
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return {"message": "Successfully logged out"}