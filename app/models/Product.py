from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.models import BaseModel
from app.models.Order import order_product_association


class Product(BaseModel):
    __tablename__ = 'products'

    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    # Relationship
    orders = relationship('Order', secondary=order_product_association, back_populates='products')
