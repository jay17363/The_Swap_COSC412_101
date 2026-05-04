"""
seed_vault.py 
run once to add ownership records for the demo account
command: python seed_vault.py
"""

from database import SessionLocal, engine
from buyBack import Base, Ownership
from datetime import datetime, timezone, timedelta

Base.metadata.create_all(bind=engine)

#User ID 1 = testAccount1@gmail.com
#pass for account if needed = Password123*
#linking demo account to products already in the DB (IDs 1-12)


OWNERSHIPS = [
    #list of dicts
    {
        "user_id": 1,
        "product_id": 1,  # Graco 4Ever DLX Car Seat
        "purchase_price": 189.99,
        "current_condition": "good",
        "purchase_date": datetime.now(timezone.utc) - timedelta(days=45),
    },
    {
        "user_id": 1,
        "product_id": 5,  # DeWalt 20V Cordless Drill
        "purchase_price": 149.99,
        "current_condition": "like-new",
        "purchase_date": datetime.now(timezone.utc) - timedelta(days=20),
    },
    {
        "user_id": 1,
        "product_id": 9,  # Husqvarna Chainsaw
        "purchase_price": 249.99,
        "current_condition": "good",
        "purchase_date": datetime.now(timezone.utc) - timedelta(days=90),
    },
]

def seed():
    db = SessionLocal()
    try:
        existing = db.query(Ownership).filter(Ownership.user_id == 1).count()
        if(existing > 0 ):
            print("User 1 already has "+ str(existing) + " ownership records. Skipping")
            return None
        
        for o in OWNERSHIPS:
            ownership = Ownership(**o) #no exponetiation its for unpacking/packing the dict
            db.add(ownership)

        db.commit()
        print("add ", len(OWNERSHIPS) , " ownership records for testAccount1")

    except Exception as e:
        db.rollback()
        print("Error: " + e)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
        