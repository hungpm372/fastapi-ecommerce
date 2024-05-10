from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.configs.database import Base
from app.models import BaseModel

order_product_association = Table('order_product', Base.metadata,
                                  Column('order_id', Integer, ForeignKey('orders.id')),
                                  Column('product_id', Integer, ForeignKey('products.id')),
                                  Column('quantity', Integer, nullable=False)
                                  )


class Order(BaseModel):
    __tablename__ = 'orders'

    total_quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship
    user = relationship('User', back_populates='orders')
    products = relationship('Product', secondary=order_product_association, back_populates='orders')
