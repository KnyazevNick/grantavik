from fastapi import FastAPI, HTTPException

from app.check_users import get_user_by_id

from app.users.schemas import UserRead, UserCreate
from app.users.services import create_user



grantavik = FastAPI(title="Grantavik")



@grantavik.get('/health')
def health():
    return {"status": "ok"}


@grantavik.get('/user/getuserbyid')
def find_user_by_id(id: int):
    result = get_user_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="user not found")


@grantavik.post('/register')
def create_user_db(user: UserCreate) -> UserRead:
    return create_user(user)
    
