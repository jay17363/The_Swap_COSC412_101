from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timezone


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


app.mount("/static", StaticFiles(directory="../Frontend/javaScript"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("../Frontend/HTML/homePage_V2.html")

# this is for the catalog
@app.get("/catalog")
def serve_catalog():
    return FileResponse("../Frontend/HTML/catalog.html")





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
        hashed_pwd=authBack.hash_password(user_in.password),
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

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(bb.Product).filter(bb.Product.is_available == True).all()

#/vault servers the HTML page 
@app.get("/vault")
def serve_vault():
    return FileResponse("../Frontend/HTML/vault.html")

#/api/vault returns json data from the DB
@app.get("/api/vault")
def get_vault (current_user: bb.User = Depends(authBack.get_current_user), db: Session = Depends(get_db)):
    #fr met for all items owned by the logged-in user with buy-back values
    ownerships = db.query(bb.Ownership).filter(bb.Ownership.user_id == current_user.id).all()

    result = []
    for o in ownerships:
        product = db.query(bb.Product).filter(bb.Product.id == o.product_id).first()


        #buy back rates per catergory FR met

        rates = {
            "baby gear": 0.60,
            "power tools": 0.65,
            "seasonal equipment": 0.55,
        }
        condition_multiplier = {
            "like-new": 1.0,
            "good":     0.85,
            "fair":     0.65,
        }
        rate = rates.get(product.category.lower(), 0.60)
        age_days = (datetime.now(timezone.utc) - o.purchase_date.replace(tzinfo=timezone.utc)).days
        multiplier = condition_multiplier.get(o.current_condition.lower(), 0.85)
        buyback_value = round(product.price * rate * multiplier * max(0.5, 1 - (age_days / 365) *0.2), 2)

        result.append({
            "ownership_id": o.id,
            "product_id": product.id,
            "name": product.name,
            "category": product.category,
            "condition": o.current_condition,
            "purchase_price": o.purchase_price,
            "purchase_date": o.purchase_date.isoformat(),
            "buyback_value": buyback_value,
        })

        #dict returned but FastAPI converts it to json 
    return { 
        "vault_credit": current_user.vault_credit,
        "items": result
    }