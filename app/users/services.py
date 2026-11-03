from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException

from app.users.schemas import UserCreate, UserRead
from app.users.passwords import hash_password

from app.users.models import User

from app.db import SessionFactory



def create_user(user: UserCreate) -> UserRead:
    """Create user in the database."""
    with SessionFactory() as session:
        password_hash = hash_password(user.password)

        new_user = User(
            username=user.username,
            password_hash=password_hash,
        )
        session.add(new_user)

        try:
            session.commit()
        except IntegrityError as error:
            session.rollback()

            sqlstate = getattr(error.orig, "sqlstate", None)
            diagnostic = getattr(error.orig, "diag", None)
            constraint_name = getattr(diagnostic, "constraint_name", None)

            if sqlstate == "23505" and constraint_name == "users_username_key":
                raise HTTPException(
                    status_code=409,
                    detail="username is already taken",
                    )

            raise

        return UserRead.model_validate(new_user)


def get_user_by_id(user_id: int) -> UserRead | None:
    """search user by id, return UserRead if found or None"""
    with SessionFactory() as session:
        statement = select(User).where(User.id == user_id)
        user = session.scalar(statement)
        if user is None:
            return None

        return UserRead.model_validate(user)


def get_user_by_username(username: str) -> UserRead | None:
    """search user by username, return UserRead if found or None"""
    with SessionFactory() as session:
        statement = select(User).where(User.username == username)
        user = session.scalar(statement)
        if user is None:
            return None

        return UserRead.model_validate(user)