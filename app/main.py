from fastapi import FastAPI, HTTPException

from app.check_users import get_user_by_id, get_user_by_username

from app.users.schemas import UserRead, UserCreate
from app.users.services import create_user, check_user
from app.users.token import create_access_token



grantavik = FastAPI(title="Grantavik")



@grantavik.get('/health')
def health():
    return {"status": "ok"}


@grantavik.get('/user/getuserbyid')
def find_user_by_id(id: int):
    result = get_user_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="user not found")
    return result


@grantavik.get('/user/getuserbyusername')
def find_user_by_username(username: str):
    result = get_user_by_username(username)
    if result is None:
        raise HTTPException(status_code=404, detail="user not found")
    return result


@grantavik.post('/auth/register')
def create_user_db(user: UserCreate) -> UserRead:
    return create_user(user)


@grantavik.post("/auth/login")
def login(user: UserCreate):
    result = check_user(user)
    if result is None:
        raise HTTPException(status_code=401, detail="invalid username or password")
    return create_access_token(result.id)