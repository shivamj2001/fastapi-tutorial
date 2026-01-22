# This file defines authentication-related API routes, such as user registration.
# This router handles incoming requests and delegates to service functions for processing.
from fastapi import APIRouter, Depends, HTTPException, status

# AsyncSession: Type hint for our non-blocking database connection
from sqlalchemy.ext.asyncio import AsyncSession

# This module provides OAuth2 password bearer token support. 
# It helps extract the token from request headers.
from fastapi.security import OAuth2PasswordRequestForm

# This module handles password hashing and JWT token creation/verification.
from app.core.security import verify_password, create_access_token

# 'select' is the tool used to write database queries (like searching for users).
from sqlalchemy import select




# The database dependency to get a session
from app.db.session import get_db
# Pydantic Schema for user registration
from app.schemas.user_request import UserRegister, UserLogin
# The service function that handles user login logic
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
# This handles user login requests, returning a JWT token upon successful authentication
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

# Look up the user by username
    result = await db.execute(
        select(User).where(User.username == form_data.username)
    )


    user = result.scalar_one_or_none()


    # Throw error if user not found or password incorrect
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    # Create JWT token for the authenticated user
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }





# This endpoint returns information about the currently authenticated user
@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }
