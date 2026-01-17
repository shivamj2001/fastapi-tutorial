# 'AsyncSession' is the type hint for our database sessions.
# 'create_async_engine' is the core function that establishes the non-blocking connection to PostgreSQL.
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# 'sessionmaker' is a utility used to create a consistent configuration for individual database sessions (tasks).
from sqlalchemy.orm import sessionmaker

# 'Settings' is our custom configuration class that pulls validated 
# credentials (user, password, host) from the .env file.
from app.core.config import Settings

# 1. Load the configuration from your .env file
settings = Settings()

# 2. Construct the Database Connection String (URL)
# We use 'postgresql+asyncpg' to tell SQLAlchemy to use the 
# asynchronous driver (asyncpg) instead of the standard synchronous one.
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:"
    f"{settings.db_password}@{settings.db_host}:"
    f"{settings.db_port}/{settings.db_name}"
)

# 3. Create the Async Engine
# This is the actual "connection manager" to the database.
# 'echo=False' means it won't print every SQL query to your console (set to True for debugging).
engine = create_async_engine(DATABASE_URL, echo=False)

# 4. Create a Session Factory (AsyncSessionLocal)
# This is a 'factory' that produces a new database session whenever we need one.
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,      # Ensures all sessions created are asynchronous
    expire_on_commit=False,   # Prevents SQLAlchemy from "refreshing" objects 
                              # automatically after a commit, which is safer for async.
)



# 'async def' allows this to run without blocking the server.
async def get_db():
    # 1. Opens a new database session from the factory.
    # The 'async with' ensures the session is cleaned up automatically.
    async with AsyncSessionLocal() as session:
        
        # 2. 'yield' sends the session to the API route.
        # It pauses here while the route uses the database.
        yield session

    # 3. Once the route is done, the code resumes and closes the session.