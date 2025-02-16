from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone  # Ensure correct imports


SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔐 Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generates a JWT access token."""
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    """Verifies if the entered password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    """Hashes a password before storing it in the database."""
    return pwd_context.hash(password)