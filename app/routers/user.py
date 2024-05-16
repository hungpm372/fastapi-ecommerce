from fastapi import APIRouter, status, HTTPException, Depends
from app.configs import get_settings, get_db_session
from app.crud.user import UserCRUD
from app.schemas import UserOut, UserUpdate
from app.utils.jwt_utils import get_current_user

settings = get_settings()
router = APIRouter()


@router.get("/{user_id}")
async def get_user(user_id: int, session: get_db_session, current_user_id: int = Depends(get_current_user)):
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db_user = await UserCRUD.get_user_by_id(user_id, session)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return dict(
        message="User retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=UserOut.model_validate(db_user)
    )


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, session: get_db_session, current_user_id: int = Depends(get_current_user)):
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    updated_user = await UserCRUD.update_user(user_id, user, session)
    return dict(
        message="User updated successfully",
        status_code=status.HTTP_200_OK,
        data=UserOut.model_validate(updated_user)
    )


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: get_db_session, current_user_id: int = Depends(get_current_user)):
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    deleted_user = await UserCRUD.delete_user(user_id, session)

    return dict(
        message="User deleted successfully",
        status_code=status.HTTP_200_OK,
        data=UserOut.model_validate(deleted_user)
   )
