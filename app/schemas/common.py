from typing import Generic, TypeVar
from pydantic import BaseModel

# 1. Define a Type Variable "T". 
# Think of "T" as a placeholder for "any type of data" (like a User, a List, or an ID).
T = TypeVar("T")

# 2. Create a Generic class that inherits from Pydantic's BaseModel.
# The 'Generic[T]' allows this class to adapt to whatever data we put inside it.
class APIResponse(BaseModel, Generic[T]):
    
    # 3. A boolean flag to tell the frontend if the operation worked.
    success: bool
    
    # 4. A human-readable message (e.g., "User created successfully" or "User not found").
    message: str
    
    # 5. The actual content of the response.
    # 'T | None = None' means:
    # - It can be of type T (the data we are sending back).
    # - It can be None (useful for errors where there is no data to return).
    # - It defaults to None if we don't provide it.
    data: T | None = None