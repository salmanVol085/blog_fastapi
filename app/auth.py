# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import jwt
# import os

# # Use Argon2
# pwd_context = CryptContext(
#     schemes=["argon2"],
#     default="argon2",
#     deprecated="auto"
# )

# SECRET = os.getenv("SECRET_KEY", "super-secret-key")
# ALGO = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain: str, hashed: str) -> bool:
#     return pwd_context.verify(plain, hashed)

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET, algorithm=ALGO)



from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os


pwd_context = CryptContext(
schemes=["argon2", "bcrypt"], # temporary backward compatibility
default="argon2",
deprecated="auto"
)


SECRET = os.getenv("SECRET_KEY", "super-secret-key")
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGO)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload
    except jwt.JWTError:
        return None