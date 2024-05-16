from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.utils.password_utils import get_password_hash


class UserCRUD:
    # Create a new user
    @staticmethod
    async def create_user(user: UserCreate, db: AsyncSession) -> User:
        user.password = get_password_hash(user.password)
        new_user = User(**user.dict())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    # Get a user by email
    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession) -> User:
        user = (await db.scalars(select(User).where(User.email == email))).first()
        return user

    # Get a user by ID
    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
        user = (await db.scalars(select(User).where(User.id == user_id))).first()
        return user

    # Update a user
    @staticmethod
    async def update_user(user_id: int, user: UserUpdate, db: AsyncSession) -> User:
        db_user = await UserCRUD.get_user_by_id(user_id, db)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user

    # Delete a user
    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession):
        db_user = await UserCRUD.get_user_by_id(user_id, db)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        await db.delete(db_user)
        await db.commit()
        return db_user
