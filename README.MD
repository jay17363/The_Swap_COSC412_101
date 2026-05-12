# The Swap
**KJJO Innovations — Towson University**  
Khurram Choudhry, Jayden Fisher 

A web platform that lets users buy short-term-use items like baby gear and power tools, and recover their cost through a guaranteed buy-back system.

---
## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python 3.10+ / FastAPI
- **Database:** SQLite via SQLAlchemy
- **Auth:** JWT tokens via python-jose / bcrypt

---

## Setup Instructions (Windows Local Computer)
 
### 1. Clone the repository

- git clone https://github.com/jay17363/The_Swap_COSC412_101
- cd The_Swap_COSC412_101

 
### 2. Activate the virtual environment
Open PowerShell/VS terminal and run:
- Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
- python -m venv venv
- .\venv\Scripts\activate

You should see `(venv)` at the start of your terminal line.

### 3. Install dependencies
- cd backend
- pip install -r requirements.txt

### 4. Seed the database with products
Run this once to populate the product catalog (while still in backend):
- python database_products.py

You should see Successfully added 12 products to the database

### 5. (Optional) Seed demo vault data
Run this once to add ownership records for the demo account:
- python seed_vault.py

### 6. Start the server
- uvicorn main:app --reload

You should see: `INFO: Application startup complete.` at the bottom

### 7. Open the app
Go to your browser and visit:
http://127.0.0.1:8000


## API endpoints
- /register - Create a new account
- /login - Login and recieve a JWT token
- /me - get current logged-in User info
- /products - Get all available products
- /api/vault - Get Owned items for logged-in user
