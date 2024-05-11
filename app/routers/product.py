from fastapi import APIRouter, status, HTTPException
from app.configs import get_settings, get_db_session
from app.crud.product import ProductCRUD
from app.schemas import ProductCreate, ProductOut, ProductUpdate

settings = get_settings()
router = APIRouter()


@router.get("")
async def get_products(session: get_db_session, skip: int = 0, limit: int = 10):
    db_products = await ProductCRUD.get_all_products(session, skip, limit)

    return dict(
        message="Products retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=[ProductOut.model_validate(product) for product in db_products]
    )


@router.get("/{product_id}")
async def get_product(product_id: int, session: get_db_session):
    db_product = await ProductCRUD.get_product_by_id(product_id, session)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return dict(
        message="Product retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=ProductOut.model_validate(db_product)
    )


@router.post("")
async def create_product(product: ProductCreate, session: get_db_session):
    new_product = await ProductCRUD.create_product(product, session)
    return dict(
        message="Product created successfully",
        status_code=status.HTTP_201_CREATED,
        data=ProductOut.model_validate(new_product)
    )


@router.put("/{product_id}")
async def update_product(product_id: int, product: ProductUpdate, session: get_db_session):
    updated_product = await ProductCRUD.update_product(product_id, product, session)
    return dict(
        message="Product updated successfully",
        status_code=status.HTTP_200_OK,
        data=ProductOut.model_validate(updated_product)
    )


@router.delete("/{product_id}")
async def delete_product(product_id: int, session: get_db_session):
    deleted_product = await ProductCRUD.delete_product(product_id, session)
    return dict(
        message="Product deleted successfully",
        status_code=status.HTTP_200_OK,
        data=ProductOut.model_validate(deleted_product)
    )
