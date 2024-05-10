from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)

    # Relationship
    payments = relationship('Payment', back_populates='user')
    orders = relationship('Order', back_populates='user')

