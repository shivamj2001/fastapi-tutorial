# 'AsyncSession' handles the non-blocking connection to your database.
from sqlalchemy.ext.asyncio import AsyncSession

# 'select' is the tool used to write database queries (like searching for users).
from sqlalchemy import select

# 'User' is your Database Model (how data is stored in PostgreSQL).
from app.models.user import User

# 'UserCreate' and 'UserUpdate' are Pydantic Schemas (how data is validated from the user).
from app.schemas.user_request import UserCreate, UserUpdate

# 'hash_password' is the function that turns plain passwords into secure hashed versions.
from app.core.security import hash_password, verify_password, create_access_token







# --- CREATE: Add a new user to the database ---
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    # 1. Turn the input data into a Database object
    new_user = User(name=user.name, age=user.age)
    db.add(new_user)            # Stage it
    await db.commit()           # Save it permanently
    await db.refresh(new_user)  # Get the new ID from the DB
    return new_user

# --- READ ALL: Get every user in the table ---
async def get_all_users(db: AsyncSession):
    # 1. Run a search for all users
    result = await db.execute(select(User))
    # 2. Convert database rows into a Python list
    return result.scalars().all()

# --- READ BY ID: Find one specific user ---
async def get_user_by_id(db: AsyncSession, user_id: int):
    # 1. Search for the user where the ID matches
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    # 2. Return the user, or None if not found
    return result.scalar_one_or_none()

# --- UPDATE: Change an existing user's info ---
async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    # 1. Find the user first
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        return None

    # 2. Apply the new name and age
    existing_user.name = user.name
    existing_user.age = user.age

    await db.commit()           # Save changes
    await db.refresh(existing_user)
    return existing_user

# --- DELETE: Permanently remove a user ---
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    # 1. Find the user first
    user = await get_user_by_id(db, user_id)
    if not user:
        return False # Nothing to delete

    # 2. Remove from session and save change
    await db.delete(user)
    await db.commit()
    return True


async def register_user(db: AsyncSession, user_data):
    # check if username already exists
    result = await db.execute(select(User).where(User.username == user_data.username))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValueError("Username already exists")
    
    # 2. Hash the password
    hashed_pw = hash_password(user_data.password)


    # 3. Create new User ORM object
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_pw,
        role="user",
        name=user_data.name,
        age=user_data.age
    )

    # 4. Add to the database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user



# --- AUTHENTICATE: Verify user credentials ---
# This function checks if the username and password are correct and returns the user if they are.
async def authenticate_user(db, username: str, password: str):
    # 1. Find the user by username
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
     
    # 2. If user not found, return None 
    if not user:
        return None
 
    # 3. Verify the password
    if not verify_password(password, user.hashed_password):
        return None

    return user


# --- LOGIN: Authenticate and return access token ---
# This function logs in the user and returns a JWT token if successful.
async def login_user(db, username: str, password: str):

    # 1. Authenticate the user
    user = await authenticate_user(db, username, password)

    # 2. If authentication fails, return None
    if not user:
        return None

    # 3. Create JWT token
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }
 
    # 4. Generate the access token
    access_token = create_access_token(token_data)
    return access_token