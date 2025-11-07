from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from utils.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__= "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="orders")