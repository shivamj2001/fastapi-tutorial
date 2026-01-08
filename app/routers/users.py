from fastapi import APIRouter, HTTPException
from app.schemas.user_request import UserCreate
from app.schemas.user_request import UserUpdate
from app.schemas.user_response import UserResponse
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user_api(user: UserCreate):
    return create_user(user)


@router.get("/", response_model=list[UserResponse])
def get_users_api():
    return get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_api(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_api(user_id: int, user: UserUpdate):
    updated_user = update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user_api(user_id: int):
    success = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
