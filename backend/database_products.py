"""
database_products.py
Run this once from the backend folder to populate the database with sample products.
Command: python database_products.py
"""

from database import SessionLocal, engine
from buyBack import Base, Product

#make sure all tables exist before we insert
Base.metadata.create_all(bind=engine)

#product_data_structure is a list but each item inside the list is a dictionary
#i.e. [ {
#        "key": "value"
#       "brand": "ford",
#        "Model": "mustang",
#        "year": 1964
# } ]
#this is one item of the list at index 0
product_data_structure =  [
    # ── Baby Gear ──
    {
        "name": "Graco 4Ever DLX Car Seat",
        "description": "4-in-1 convertible car seat that grows with your child from infant to booster. Side impact protection included.",
        "category": "baby gear",
        "condition": "like-new",
        "price": 189.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "UPPAbaby VISTA Stroller",
        "description": "Full-size stroller with extendable canopy, large storage basket, and adjustable handlebar. Fits infant bassinet.",
        "category": "baby gear",
        "condition": "good",
        "price": 299.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "IKEA SNIGLAR Crib",
        "description": "Solid beech wood crib. Fits standard crib mattress. Simple, sturdy design. Mattress not included.",
        "category": "baby gear",
        "condition": "good",
        "price": 89.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "Graco DuetSoothe Swing",
        "description": "Baby swing with 6 speeds, 10 songs, and nature sounds. Converts to a rocker. Gently used.",
        "category": "baby gear",
        "condition": "fair",
        "price": 74.99,
        "photo_url": None,
        "is_available": True,
    },
 
    # ── Power Tools ──
    {
        "name": "DeWalt 20V Cordless Drill",
        "description": "Brushless motor, 2-speed transmission, 1/2 inch chuck. Includes 2 batteries and charger.",
        "category": "power tools",
        "condition": "like-new",
        "price": 149.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "Milwaukee M18 Circular Saw",
        "description": "7-1/4 inch blade, 18V lithium-ion. Cuts through 2x lumber with ease. Battery not included.",
        "category": "power tools",
        "condition": "good",
        "price": 129.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "Ryobi 18V Brad Nailer",
        "description": "Cordless brad nailer, 18 gauge. No compressor needed. Fires up to 700 nails per charge.",
        "category": "power tools",
        "condition": "good",
        "price": 99.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "Makita Random Orbital Sander",
        "description": "5 inch pad, variable speed dial, dust collection bag included. Great for finish sanding.",
        "category": "power tools",
        "condition": "fair",
        "price": 59.99,
        "photo_url": None,
        "is_available": True,
    },
 
    # ── Seasonal Equipment ──
    {
        "name": "Husqvarna 450 Rancher Chainsaw",
        "description": "20 inch bar, 50.2cc engine. Ideal for cutting firewood and felling medium trees.",
        "category": "seasonal equipment",
        "condition": "good",
        "price": 249.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "Toro 21 inch Snow Blower",
        "description": "Single stage electric start snow blower. Clears up to 21 inch wide path. Barely used.",
        "category": "seasonal equipment",
        "condition": "like-new",
        "price": 319.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "Sun Joe Electric Pressure Washer",
        "description": "1750 PSI, 1.5 GPM. Includes 5 spray nozzles and 20 ft high pressure hose.",
        "category": "seasonal equipment",
        "condition": "good",
        "price": 109.99,
        "photo_url": None,
        "is_available": True,
    },
    {
        "name": "Black+Decker 40V Leaf Blower",
        "description": "Cordless leaf blower, 120 MPH airspeed. Lightweight at 4.8 lbs. Battery and charger included.",
        "category": "seasonal equipment",
        "condition": "like-new",
        "price": 79.99,
        "photo_url": None,
        "is_available": True,
    },
]

def link ():
    db=SessionLocal()
    try:
        #check if products already exist so there are no double entries and if there is 50 of the same item you could just buy the one listing 50 times
        existing = db.query(Product).count()
        if (existing) > 0:
           print("Database already has ", existing, "products. Skipping link") 
           print("If you want to re-link, delete the_swap.dp and run again")
           return None
        for p in product_data_structure:
            prod = Product(**p) #**p takes the current dictionary key and value pairs and unpacks them so they act like keyword args
            db.add(prod)
        
        db.commit()
        print("Successfully added ", len(product_data_structure), "products to the database.")


        print("\n Products added: ")
        for p in product_data_structure:
            print("  [" + p['category'] + "] " + p['name'] + " — $" + str(p['price']))
    
    except Exception as e:
        db.rollback()
        print("Error linking database with products: ", {e})
    finally:
        db.close()


if __name__ == "__main__":
    link()
