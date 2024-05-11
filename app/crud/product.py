from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Product
from fastapi import status, HTTPException
from app.schemas import ProductCreate, ProductUpdate


class ProductCRUD:
    # The create_product method creates a new product in the database.
    @staticmethod
    async def create_product(product: ProductCreate, db: AsyncSession) -> Product:
        new_product = Product(**product.dict())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    # The get_product_by_id method retrieves a product from the database by its ID.
    @staticmethod
    async def get_product_by_id(product_id: int, db: AsyncSession) -> Product:
        product = (await db.scalars(select(Product).where(Product.id == product_id))).first()
        return product

    # The get_all_products method retrieves all products from the database.
    @staticmethod
    async def get_all_products(db: AsyncSession, skip: int, limit: int):
        products = await db.execute(select(Product).offset(skip).limit(limit))
        return products.scalars().all()

    # The update_product method updates a product in the database.
    @staticmethod
    async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession) -> Product:
        db_product = await ProductCRUD.get_product_by_id(product_id, db)
        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        for key, value in product.dict().items():
            setattr(db_product, key, value)

        await db.commit()
        await db.refresh(db_product)
        return db_product

    # The delete_product method deletes a product from the database.
    @staticmethod
    async def delete_product(product_id: int, db: AsyncSession):
        db_product = await ProductCRUD.get_product_by_id(product_id, db)
        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        await db.delete(db_product)
        await db.commit()
        return db_product
