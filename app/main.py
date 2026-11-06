from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.users.schemas import UserRead, UserCreate, TokenRead
from app.users.services import create_user, check_user, get_user_by_id, get_user_by_username
from app.users.token import create_access_token, decode_access_token



grantavik = FastAPI(title="Grantavik")
bearer = HTTPBearer(auto_error=False)



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
def login(user: UserCreate) -> TokenRead:
    checked_user = check_user(user)
    if checked_user is None:
        raise HTTPException(status_code=401, detail="invalid username or password")
    return TokenRead(access_token=create_access_token(checked_user.id))


@grantavik.get('/auth/me')
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    ) -> UserRead:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )

    token = credentials.credentials
    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )

    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )

    return user