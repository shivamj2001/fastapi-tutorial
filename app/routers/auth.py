# This file defines authentication-related API routes, such as user registration.
# This router handles incoming requests and delegates to service functions for processing.
from fastapi import APIRouter, Depends, HTTPException

# AsyncSession: Type hint for our non-blocking database connection
from sqlalchemy.ext.asyncio import AsyncSession


# The database dependency to get a session
from app.db.session import get_db
# Pydantic Schema for user registration
from app.schemas.user_request import UserRegister, UserLogin
from app.services.user_service import login_user

# The service function that handles user registration logic
from app.services.user_service import register_user

# Dependency to get the current authenticated user
from app.core.dependencies import get_current_user
# The User database model
from app.models.user import User

# --- ROUTER SETUP ---
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# This endpoint allows new users to register
@router.post("/register")
# This function handles user registration requests
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    # Try to register the user using the service function
    try:
        new_user = await register_user(db, user)
        return {
            "message": "User registered successfully",
            "username": new_user.username,
            "role": new_user.role
        }
    # Handle errors such as username already taken
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


# This endpoint allows users to log in and receive an access token
@router.post("/login")
# This function handles user login requests
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):

    # Call the service function to authenticate and get a token
    token = await login_user(db, user.username, user.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 
@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }
