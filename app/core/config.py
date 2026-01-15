from pydantic_settings import BaseSettings

# Settings inherits from BaseSettings, which tells Pydantic to look for 
# environment variables or a .env file to fill these values.
class Settings(BaseSettings):
    
    # --- General App Settings ---
    # These have 'default values'. If they aren't in your .env, it uses these.
    app_name: str = "FastAPI Tutorial"
    debug: bool = False

    # --- Database Credentials ---
    # These do NOT have default values. 
    # The app will CRASH on startup if these are missing from your .env.
    # This is a safety feature called "Validation".
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # --- Internal Config ---
    class Config:
        # This tells Pydantic to look for a file named ".env" 
        # in the root directory to find the values above.
        env_file = ".env"