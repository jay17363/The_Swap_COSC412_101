from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db

import buyBack as bb
import schemas
import authBack

# Create all tables defined in buyBack.
bb.Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Swap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allows all websites (good for development)
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Message": "The Swap backend is up and running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "tables": list(bb.Base.metadata.tables.keys())}


# --- Auth routes ---

@app.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """FR#1, FR#2, FR#3 — create a new account."""
    # FR#2: check email isn't already taken
    existing = db.query(bb.User).filter(bb.User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with that email already exists",
        )

    new_user = bb.User(
        email=user_in.email,
        hashed_pwd=authBack.hashed_pwd(user_in.password),
        display_name=user_in.display_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # populates new_user.id from the DB
    return new_user


@app.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """FR#5 — log in and get a token."""
    user = db.query(bb.User).filter(bb.User.email == credentials.email).first()
    if not user or not authBack.verify_password(credentials.password, user.hashed_pwd):
        # Same error for "no user" and "wrong password" — don't leak which it was.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = authBack.create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: bb.User = Depends(authBack.get_current_user)):
    """Returns info about the currently logged-in user. Useful for testing the token works."""
    return current_user