from pydantic import BaseModel, EmailStr, ConfigDict


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    price: int
    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductIn(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
