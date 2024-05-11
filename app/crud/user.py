from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.schemas import UserOut, UserCreate, UserUpdate
from app.utils.password_utils import get_password_hash


# Create a new user
async def create_user(user: UserCreate, db: AsyncSession) -> User:
    user.password = get_password_hash(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# Get a user by email
async def get_user_by_email(email: str, db: AsyncSession) -> User:
    user = (await db.scalars(select(User).where(User.email == email))).first()
    return user


# Get a user by ID
async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    user = (await db.scalars(select(User).where(User.id == user_id))).first()
    return user
