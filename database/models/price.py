from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database.connection import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))

    price = Column(Float, nullable=False)
    currency = Column(String, default="CAD")

    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product")
    store = relationship("Store", back_populates="prices")