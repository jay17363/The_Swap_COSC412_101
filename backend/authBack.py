from datetime import datetime, timedelta, timezone #used to set token expiration times
from jose import JWTError, jwt #used to create and decode JWT tokens (our login tokens)

#FastAPI import Depends injects dependeices, HTTPExecptions sends error responses,
# status gives us clean status cods like 401, 400
from fastapi import Depends, HTTPException, status

#tells FastAPI to look for a bearer token
from fastapi.security import OAuth2PasswordBearer

#used for type hints on database functions 
from sqlalchemy.orm import Session

#our files get_db gives us a DB session, Users is the users tables models
from database import get_db
from buyBack import User

#used to make sure we are hashing passwords securely 
import bcrypt



# In a real app, this would come from an environment variable.
# For our prototype, hardcoded is fine 
SECRET_KEY = "kjjo-the-swap-dev-secret-change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # token valid for 1 hour


# This tells FastAPI to look for a Bearer token in the Authorization header.
# tokenUrl="login" is for the auto-generated /docs page.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Password helpers

def hash_password(password: str) -> str:
    """One-way hash a plain password for storage."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_pwd: str) -> bool:
    """Check if a plain password matches the stored hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_pwd.encode("utf-8"))

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
    #define the error we'll throw anytime the token is missing, invalid or expired
    #401 = Unauthorized 
    #WWW-Authenticate header is formal way to write it 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #decode the JWT token using our secret key and algorithm
    #this verifies the signature and checks the expiration time 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # "sub" (subject) is the field we stored the user's ID 
        user_id_str: str | None = payload.get("sub")
        
        #if there is no sub field in the token payload something went wrong 
        if user_id_str is None:
            raise credentials_exception
        #convert the user ID from string to int so we can query the database with it 
        user_id = int(user_id_str)
    
    #if the token is expired or invalid, reject it
    except JWTError:
        raise credentials_exception
    #look up the user in the database using the id from the token
    user = db.query(User).filter(User.id == user_id).first()

    #if the user no longer exists in the DB - reject it 
    if user is None:
        raise credentials_exception
    
    #token is valid and the user is real return it
    return user