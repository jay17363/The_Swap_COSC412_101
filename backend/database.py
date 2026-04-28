from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

# SQLite database file. Will be created at backend/the_swap.db when first used.
SQLALCHEMY_DATABASE_URL = "sqlite:///./the_swap.db"


# The engine is the connection pool to the database.
# check_same_thread=False is required for SQLite + FastAPI (FastAPI uses multiple threads).

#thread
engine = create_engine (
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# A SessionLocal is a database session: one conversation with the database
#we'll create one per request, then close it when the request is done 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Base is the parent class our table models(buy back) will inherit from.

Base = declarative_base()

# Dependency function FastAPI uses to give each request its own DB session.
def get_db():
    db = SessionLocal() #1. open data base 
    try:
        yield db # 2. handle it to the route fucntion. pause here
        #yield puases the function 
        #no except right now becuase of no error known 
    finally:
        db.close()#3. after the route is done. resume. close the session

