from fastapi import FastAPI

from app.users.schemas import UserRead, UserCreate
from app.users.services import create_user



grantavik = FastAPI(title="Grantavik")



@grantavik.get('/health')
def health():
    return {"status": "ok"}


@grantavik.post('/register')
def create_user_db(user: UserCreate) -> UserRead:
    return create_user(user)
    
