from sqlalchemy import select

from app.db import SessionFactory

from app.users.models import User
from app.users.schemas import UserRead


def print_all_users(): #function for console
    with SessionFactory() as session:
        statement = select(User)
        users = session.scalars(statement).all()
        for user in users:
            user_read = UserRead.model_validate(user)
            print(user_read.model_dump())


def print_all_usernames(): #function for console
    with SessionFactory() as session:
        statement = select(User.username)
        users = session.scalars(statement).all()
        print(users)


#work function
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