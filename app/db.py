from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings



class Base(DeclarativeBase):
    pass


database_url = URL.create(
    "postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(database_url)