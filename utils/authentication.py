from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from database.models import RegisteredUser
from database.helpers import session_scope
from rest.models import UserInDB, TokenData
from settings import ALGORITHM, SECRET_KEY, oauth2_scheme, pwd_context


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    with session_scope() as session:
        user = session.query(RegisteredUser).filter(RegisteredUser.username == username).first()
    if user:
        return UserInDB(
            username=user.username,
            name=user.name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
        )


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    elif not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_credentials(token: str = Depends(oauth2_scheme)):
    """Check if credentials are valid else raise a HTTPError"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as error:
        raise credentials_exception from error
    else:
        user = get_user(username=token_data.username)  # type: ignore
        if user is None:
            raise credentials_exception
