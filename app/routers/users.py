from fastapi import APIRouter, HTTPException
from schemas.user_request import UserCreate
from schemas.user_response import UserResponse
from services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id
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
