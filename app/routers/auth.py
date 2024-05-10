from datetime import timedelta

from fastapi import APIRouter, status, HTTPException
from app.configs import get_settings, get_db_session
from app.crud.user import get_user_by_email, create_user
from app.schemas import UserCreate, UserIn, UserOut
from app.utils.jwt_utils import create_access_token
from app.utils.password_utils import verify_password

settings = get_settings()
router = APIRouter()


@router.post('/sign-up')
async def sign_up(user: UserCreate, session: get_db_session):
    db_user = await get_user_by_email(user.email, session)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = await create_user(user, session)
    return dict(
        message="User created successfully",
        status_code=status.HTTP_201_CREATED,
        data=UserOut.model_validate(new_user)
    )


@router.post('/sign-in')
async def sign_in(user: UserIn, session: get_db_session):
    db_user = await get_user_by_email(user.email, session)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.id}, expires_delta=expires_delta)

    return {
        "message": "User signed in successfully",
        "status_code": status.HTTP_200_OK,
        "data": {
            **UserOut.model_validate(db_user).dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }
    }
