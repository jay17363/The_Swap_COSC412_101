from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

import re


#user schemas 

class UserCreate(BaseModel):
    """Shape of the request body when someone registers."""

    email: EmailStr # fr#2

    password: str

    display_name: Optional[str]=None 
    #Oringal:::display_name: str |None = None

    @field_validator("password")
    @classmethod
    def password_strength(this_class, the_password:str) ->str:
        #raise ValueError -- is saying something went wrong, then stopping the execution and then announcs the problem 
        if len(the_password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", the_password):
            raise ValueError("Password must contain an uppercase letter")
        if not re.search(r"\d", the_password):
            raise ValueError("Passowrd most contain a number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]"):
            raise ValueError("Password must contain a special character")
        return the_password
    
class UserLogin(BaseModel):
    """Shape of the request body when someone logs in."""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """Shape of user data we send BACK to the client. Notice: no password fields."""
    id: int
    email: EmailStr
    display_name: str | None
    vault_credit: float
    is_admin: bool
    created_at: datetime

    class config:
        from_attributes = True  # lets Pydantic read from a SQLAlchemy object

#token schemas

class Token(BaseModel):
    """the response when login succeeds"""

    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """the payload we encode inside the JWT (jason web token)"""

    user_id: int | None = None
