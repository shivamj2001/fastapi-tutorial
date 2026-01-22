# APIRouter: Groups your routes; HTTPException: Sends error codes; Depends: Injects database sessions
from fastapi import APIRouter, HTTPException, Depends
# AsyncSession: Type hint for our non-blocking database connection
from sqlalchemy.ext.asyncio import AsyncSession

# Pydantic Schemas: Define how data should look for requests and responses
from app.schemas.user_request import UserCreate, UserUpdate
from app.schemas.user_response import UserResponse


from app.core.dependencies import require_role # Role-based access control dependency

# Service Functions: The logic that actually talks to PostgreSQL
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

# Database Dependency: Opens and closes the session for each request
from app.db.session import get_db

# --- ROUTER SETUP ---
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# --- ENDPOINTS ---

# 1. CREATE: Create a new user
@router.post("/", response_model=UserResponse)
async def create_user_api(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Calls the service and waits for the database to save the user
    return await create_user(db, user)

# 2. READ ALL: Get a list of all users
@router.get("/", response_model=list[UserResponse])
async def get_users_api(db: AsyncSession = Depends(get_db)):
    # Fetches all users and automatically converts them to a JSON list
    return await get_all_users(db)

# 3. READ ONE: Get a single user by their ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_api(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        # Returns a 404 error if the ID doesn't exist in the DB
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 4. UPDATE: Change details for an existing user
@router.put("/{user_id}", response_model=UserResponse)
async def update_user_api(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# 5. DELETE: Remove a user from the database
@router.delete("/{user_id}")

# This endpoint requires the current user to have the 'admin' role, enforced by the 'require_role' dependency.
async def delete_user_api(user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_role("admin"))):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    # Returns a simple confirmation message
    return {"message": "User deleted successfully"}