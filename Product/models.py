from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Boolean)
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="products")


class Seller(Base): 
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    email = Column(String)
    products = relationship("Product", back_populates="seller")
    password = Column(String)
    phone = Column(Integer)

