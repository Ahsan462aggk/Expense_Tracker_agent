

from sqlmodel import Session, select
from typing import Optional
from app.models.user import User
from passlib.hash import bcrypt


def create_user(session: Session, user: User, password: str) -> User:
    user.hashed_password = bcrypt.hash(password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user
