
from pydantic import BaseModel

# This class defines the structure of the JSON data that will be 
# sent BACK to the user after a successful request.
class UserResponse(BaseModel):
    
    # 1. The unique identifier from the database.
    # While 'UserCreate' doesn't have an ID (because it hasn't been made yet),
    # 'UserResponse' must include it so the frontend knows which user it's looking at.
    id: int
    
    # 2. The user's name as a string.
    name: str
    
    # 3. The user's age as an integer.
    age: int