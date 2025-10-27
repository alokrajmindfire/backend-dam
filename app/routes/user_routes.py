from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config.dbconf import SessionLocal
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    """
    Dependency function that provides a database session for request handling.

    Yields:
        Session: A SQLAlchemy session instance for interacting with the database.

    Ensures:
        The session is closed after the request completes, even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Retrieve a list of all registered users.

    Args:
        db (Session): Database session provided by the dependency injection system.

    Returns:
        list[UserResponse]: A list of user details, including email, and profile data.

    Raises:
        HTTPException: May be raised by controller methods if database access fails.
    """
    controller = UserController(db)
    return controller.get_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Retrieve details of a specific user by ID.

    Args:
        user_id (int): The unique identifier of the user.
        db (Session): Database session provided by the dependency injection system.

    Returns:
        UserResponse: The user’s details if found.

    Raises:
        HTTPException: 404 error if the user with the given ID does not exist.
    """
    controller = UserController(db)
    user = controller.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
def create_user(user_create: UserCreate, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
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

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Update an existing user's information.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): Schema containing updated user information.
        db (Session): Database session provided by the dependency injection system.

    Returns:
        UserResponse: The updated user's information.

    Raises:
        HTTPException: 404 error if the user with the specified ID does not exist.
    """
    controller = UserController(db)
    user = controller.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Delete a user from the database.

    Args:
        user_id (int): The unique identifier of the user to delete.
        db (Session): Database session provided by the dependency injection system.

    Returns:
        UserResponse: The details of the deleted user.

    Raises:
        HTTPException: 404 error if the user with the given ID does not exist.
    """
    controller = UserController(db)
    user = controller.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
