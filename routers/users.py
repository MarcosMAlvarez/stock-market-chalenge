from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database.models import RegisteredUser
from database.helpers import session_scope
from rest.models import UserInDB, Token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from utils import authentication

router = APIRouter()


@router.post("/sign-up", tags=["users"], status_code=status.HTTP_201_CREATED)
async def sign_up(user_to_register: UserInDB):
    """Endpoint to register a new user. Both username and email address must be unique"""
    with session_scope() as session:
        registered_user = (
            session.query(RegisteredUser)
            .filter(RegisteredUser.username == user_to_register.username)
            .first()
        )
        registered_email = (
            session.query(RegisteredUser)
            .filter(RegisteredUser.email == user_to_register.email)
            .first()
        )
        if registered_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_to_register.username} already exist in database",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if registered_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_to_register.email} already exist in database",
                headers={"WWW-Authenticate": "Bearer"},
            )
        session.add(
            RegisteredUser(
                username=user_to_register.username,
                name=user_to_register.name,
                last_name=user_to_register.last_name,
                email=user_to_register.email,
                password=user_to_register.password,
            )
        )
        session.commit()
    return {"msg": "User has been successfully registered"}


@router.post("/token", tags=["users"], response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """An authorized user can log in to get a token"""
    user = authentication.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
