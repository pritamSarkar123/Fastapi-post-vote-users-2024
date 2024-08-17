import os
from datetime import datetime, timedelta, timezone

from dotenv import find_dotenv, load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..config import settings
from ..database import Session, engine, get_db
from ..exceptions import UserNotFound
from ..models import User
from ..schemas import auth_schemas

# load_dotenv(find_dotenv())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login")
# SECRET_KEY
# Algorithm
# expiration time
# SECRET_KEY = os.environ.get("SECRET_KEY")
# ALGORITHM = os.environ.get("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

# 3 for secret key
# openssl rand -hex 32
# openssl rand -hex 64
# openssl rand -hex 128

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    endoced_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return endoced_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    endoced_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return endoced_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = auth_schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    cu = verify_token(token, credentials_exception)
    current_user = db.query(User).filter(User.id == cu.id).first()
    if not current_user:
        raise UserNotFound(cu.id)
    return current_user
