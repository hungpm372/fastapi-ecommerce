from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.configs.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
