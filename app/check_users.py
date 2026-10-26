from sqlalchemy import select

from app.db import SessionFactory

from app.users.models import User



with SessionFactory() as session:
    statement = select(User)
    users = session.scalars(statement).all()
    print(users)