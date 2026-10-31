from sqlalchemy import select

from app.db import SessionFactory

from app.users.models import User
from app.users.schemas import UserRead



with SessionFactory() as session:
    statement = select(User)
    users = session.scalars(statement).all()
    for user in users:
        user_read = UserRead.model_validate(user)
        print(user_read.model_dump())