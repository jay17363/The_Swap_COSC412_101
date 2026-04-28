from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from buyBack import User



# In a real app, this would come from an environment variable.
# For our prototype, hardcoded is fine 
SECRET_KEY = "kjjo-the-swap-dev-secret-change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # token valid for 1 hour

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This tells FastAPI to look for a Bearer token in the Authorization header.
# tokenUrl="login" is for the auto-generated /docs page.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Password helpers

def hash_password(password: str) -> str:
    """One-way hash a plain password for storage."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_pwd: str) -> bool:
    """Check if a plain password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_pwd)


# Token helpers 

def create_access_token(user_id: int) -> str:
    """Generate a signed JWT containing the user's ID and an expiration time."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# The "who is logged in?" dependency 

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Used as a FastAPI dependency on protected routes.
    Decodes the token, looks up the user, returns the User object.
    Raises 401 if the token is missing/invalid/expired or the user no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user