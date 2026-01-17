# 'AsyncSession' handles the non-blocking connection to your database.
from sqlalchemy.ext.asyncio import AsyncSession

# 'select' is the tool used to write database queries (like searching for users).
from sqlalchemy import select

# 'User' is your Database Model (how data is stored in PostgreSQL).
from app.models.user import User

# 'UserCreate' and 'UserUpdate' are Pydantic Schemas (how data is validated from the user).
from app.schemas.user_request import UserCreate, UserUpdate








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