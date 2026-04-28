from fastapi import FastAPI 
from database import engine
import buyBack as bb

# Create all tables defined in buyBack.
# If they already exist, this is a no-op. If the DB file doesn't exist, then create it.
bb.Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Swap API")


@app.get("/")
def read_root():
    return {"Message": "The Swap backend is up and running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "tables": list(bb.Base.metadata.tables.keys())}