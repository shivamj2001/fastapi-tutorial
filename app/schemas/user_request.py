# This file defines Pydantic schemas for user-related requests.
# These schemas are used to validate and structure data for creating and updating users.
from pydantic import BaseModel, field_validator, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str  # Must be a string
    age: int   # Must be an integer

    # --- CUSTOM VALIDATION ---
    # This function runs automatically whenever a new UserCreate is made
    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        # 'v' is the value being passed for age
        if v < 0:
            # If age is -5, the app stops here and returns a 422 error to the user
            raise ValueError("Age must be positive")
        
        # Always return the value if it is valid
        return v


class UserUpdate(BaseModel):
    # 'Optional' and '= None' mean these fields are NOT required.
    # This allows for "Partial Updates" (e.g., updating the name without changing the age).
    name: Optional[str] = None
    age: Optional[int] = None


# This schema is for user registration, including username and password
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    name: str
    age: int


# Schema for user login
class UserLogin(BaseModel):
    username: str
    password: str
