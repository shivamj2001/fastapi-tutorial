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
from app.models.user import User
# This module provides JWT configuration constants.
from app.core.security import SECRET_KEY, ALGORITHM

# Reads token from: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# This function retrieves the current authenticated user based on the JWT token.
async def get_current_user(
    token: str = Depends(oauth2_scheme),
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
