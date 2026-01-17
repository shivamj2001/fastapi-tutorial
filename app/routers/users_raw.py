from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.user_request import UserCreate
from app.schemas.user_request import UserUpdate
from app.schemas.user_response import UserResponse
from app.services.audit_service import audit_log
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

# Creates a sub-group of routes. 
# 'prefix="/users"' means all these URLs start with /users
# 'tags=["Users"]' groups them together in the Swagger/OpenAPI documentation.
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user_api(user: UserCreate, background_tasks: BackgroundTasks):
    # 1. Call the database logic to save the user
    new_user = create_user(user)

    # 2. Schedule the slow 'audit_log' to run in the background.
    # This allows the API to return a response immediately without waiting 1 second.
    background_tasks.add_task(audit_log, "CREATE_USER", f"User {new_user.id} created")
    
    # 3. Return the new user (FastAPI automatically formats this as UserResponse)
    return new_user


@router.get("/", response_model=list[UserResponse])
def get_users_api():
    # Simply calls the service and returns the list of user objects.
    return get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_api(user_id: int):
    user = get_user_by_id(user_id)
    # Error Handling: If the database returns None, we stop and send a 404 error.
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_api(user_id: int, user: UserUpdate):
    # Passes both the 'Who' (user_id) and the 'What' (user) to the service.
    updated_user = update_user(user_id, user)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user_api(user_id: int):
    success = delete_user(user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Returns a simple confirmation message instead of a full UserResponse.
    return {"message": "User deleted successfully"}

