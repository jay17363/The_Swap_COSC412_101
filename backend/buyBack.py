from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column (Integer, primary_key=True, index=True)
    email = Column(String, unique =True, index=True, nullable=False)
    hashed_pwd = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    shipping_address = Column(String, nullable=True)
    vault_credit = Column(Float, default=0.0)  # FR#20: vault credit balance
    is_admin = Column(Boolean, default=False)  # for FR#29 admin role check
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


    #one user can own many items 
    ownerShip = relationship ("Ownership", back_populates="owner")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False, index=True)  # baby gear, power tools, seasonal
    condition = Column(String, nullable=False)  # new, like-new, good, fair
    price = Column(Float, nullable=False)
    photo_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)  # FR#12: availability status
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    #same thing
    ownerships = relationship("Ownership", back_populates="product")


class Ownership(Base):
    """Records that user X owns a specific instance of product Y. Powers the User Vault."""

    __tablename__ = "ownerships"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    purchase_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    purchase_price = Column(Float, nullable=False)
    current_condition = Column(String, default="good")  # user can update over time

    owner = relationship("User", back_populates="ownerships")
    product = relationship("Product", back_populates="ownerships")
    quotes = relationship("BuyBackQuote", back_populates="ownership")

class BuyBackQuote(Base):
    """Logs every buy-back calculation (FR#28: log every quote for debugging)."""

    __tablename__ = "buyBack_quotes"

    id = Column(Integer, primary_key=True, index=True)
    ownership_id = Column(Integer, ForeignKey("ownerships.id"), nullable=False)
    quote_amount = Column(Float, nullable=False)
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # Inputs used, stored as plain strings for the log
    input_category = Column(String)
    input_condition = Column(String)
    input_age_days = Column(Integer)

    ownership = relationship("Ownership", back_populates="quotes")
