from app.users.schemas import UserCreate, UserRead
from app.users.passwords import hash_password

from app.users.models import User

from app.db import SessionFactory



def create_user(user: UserCreate) -> UserRead:
    """create user in data base"""
    with SessionFactory() as session:
        password_hash = hash_password(user.password)

        new_user = User(
            username=user.username,
            password_hash=password_hash,
        )

        session.add(new_user)
        session.commit()

        return UserRead.model_validate(new_user)
        