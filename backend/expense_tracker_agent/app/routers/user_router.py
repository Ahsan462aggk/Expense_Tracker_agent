from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.controllers.user_controller import create_user, authenticate_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.schemas.token_with_user import TokenWithUser
from app.auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.config.database import get_session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
import os

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserRead)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    user = User(
        username=user_create.username,
        email=user_create.email,
    )
    try:
        user = create_user(session, user, user_create.password)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    return user

@router.post("/login", response_model=TokenWithUser)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    secure_cookie = os.getenv("SECURE_COOKIE", "False").lower() in ("true", "1", "t")
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=secure_cookie,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserRead.from_orm(user)  # Include user information
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out."}
