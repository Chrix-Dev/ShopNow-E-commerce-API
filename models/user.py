from sqlalchemy import Column, Integer, String, Boolean
from utils.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,  nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Integer, default=1)
    is_verified = Column(Boolean, default=False)

    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")