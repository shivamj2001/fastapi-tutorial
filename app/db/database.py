from psycopg2 import pool
from app.core.config import Settings

# 1. Initialize the Settings object we defined.
# This reads the .env file and validates the database credentials.
settings = Settings()

# 2. Create a 'SimpleConnectionPool' instance.
# This manages a set of connections to PostgreSQL database.
db_pool = pool.SimpleConnectionPool(
    # 3. The minimum number of connections to keep open at all times.
    minconn=1,
    
    # 4. The maximum number of connections the pool can open.
    # This protects database from being overwhelmed by too many requests.
    maxconn=5,
    
    # 5. Connection details pulled directly from our validated Settings object.
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
)
