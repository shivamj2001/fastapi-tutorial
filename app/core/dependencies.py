# These dependencies file provides reusable components for FastAPI routes,
# such as getting the current authenticated user from a JWT token.
from fastapi import Depends, HTTPException, status

# This module provides OAuth2 password bearer token support.
from fastapi.security import OAuth2PasswordBearer

# This module handles JWT creation and verification.
from jose import JWTError, jwt

# AsyncSession: Type hint for our non-blocking database connection
from sqlalchemy.ext.asyncio import AsyncSession
# 'select' is the tool used to write database queries (like searching for users).
from sqlalchemy import select

from app.db.session import get_db

# The User database model
from app.models.user import User

# This module provides JWT configuration constants.
from app.core.security import SECRET_KEY, ALGORITHM

# Reads token from: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# This function retrieves the current authenticated user based on the JWT token.
async def get_current_user(
    # The token is passed in from the OAuth2 scheme, OAuth2_scheme reads it from the request header.
    token: str = Depends(oauth2_scheme),
    #
    db: AsyncSession = Depends(get_db)
): # Get the DB session
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token to get the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
   
   # Look up the user in the database
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


# This dependency ensures that the current user has the required role.
# 'required_role' is the role needed to access a particular route, e.g., 'admin'.
def require_role(required_role: str):
    # This inner function checks the user's role.
    # 'current_user' is injected via the 'get_current_user' dependency.
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user

    return role_checker
