from fastapi import Request, HTTPException, Depends
from app.config.config import settings
from sqlalchemy.orm import Session
import jwt
from app.config.dbconf import get_db
from app.models.user_model import User



def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Middleware-like dependency to verify JWT token from cookies
    and return the authenticated user.
    """
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")

    try:
        # Decode and verify token
        payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch user from DB
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
