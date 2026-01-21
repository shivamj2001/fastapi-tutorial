# done pip install passlib[bcrypt]==3.2.2

# This module handles password hashing and verification using the Passlib library.
from passlib.context import CryptContext

# This module handles JWT creation and verification.
# We use 'jose' for working with JSON Web Tokens.
from datetime import datetime, timedelta
# jwt and JWTError are used for encoding and decoding JWTs, installed via 'pip install python-jose'
from jose import jwt, JWTError

# JWT configuration
# These should be set to secure values in a real application
SECRET_KEY = "CHANGE_ME_TO_A_RANDOM_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Function to create a JWT token
# 'data' is a dictionary containing user info to encode in the token
# 'expires_delta' is an optional timedelta for token expiration time
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a signed JWT token containing user data.
    """
    # Copy the data to avoid modifying the original
    to_encode = data.copy()

    # Set the expiration time for the token 
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    # Encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# This object manages password hashing schemes and settings.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """ Take a plain password and return its hashed version. """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Check if the provided plain password matches the hashed password. """

    return pwd_context.verify(plain_password, hashed_password)