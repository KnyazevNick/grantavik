from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase
import os



class Base(DeclarativeBase):
    pass


database_url = URL.create(
    "postgresql+psycopg",
    username="grantavik_app",
    password=os.environ["GRANTAVIK_DB_PASSWORD"],
    host="localhost",
    port=5432,
    database="grantavik_db",
)

engine = create_engine(database_url)