from jose import jwt

from passlib.context import CryptContext

from datetime import datetime, timedelta

from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import (
    OAuth2PasswordBearer
)

from sqlalchemy.orm import Session

from database import SessionLocal

import models


# ================================
# JWT CONFIG
# ================================
SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ================================
# PASSWORD HASHING
# ================================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ================================
# OAUTH2
# ================================
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


# ================================
# HASH PASSWORD
# ================================
def hash_password(password: str):

    return pwd_context.hash(password)


# ================================
# VERIFY PASSWORD
# ================================
def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ================================
# CREATE TOKEN
# ================================
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ================================
# DATABASE
# ================================
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ================================
# GET CURRENT USER
# ================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if user is None:
        raise credentials_exception

    return user