from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import secrets

from app.users.schemas import UserRead, UserLogin, CreateUserRequest, UserCreated, TokenRead
from app.users.services import UsernameAlreadyTakenError, check_user, get_user_by_id, get_user_by_username, get_user_role_names, can_create_user_with_role, create_user_with_role
from app.users.token import create_access_token, decode_access_token



grantavik = FastAPI(title="Grantavik")
bearer = HTTPBearer(auto_error=False)



@grantavik.get('/health')
def health():
    return {"status": "ok"}


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


@grantavik.post('/users', status_code=201)
def create_user_db(
    user: CreateUserRequest,
    creator: UserRead = Depends(get_current_user),
    ) -> UserCreated:
    creator_roles = get_user_role_names(creator.id)
    can_create = can_create_user_with_role(creator_roles, user.role_name)
    if not can_create:
        raise HTTPException(
            status_code=403,
            detail="Not allowed to create a user with this role",
        )
    temporary_password = secrets.token_urlsafe(12)
    try:
        created_user = create_user_with_role(
            user.username,
            temporary_password,
            user.role_name,
            )
    except UsernameAlreadyTakenError as error:
        raise HTTPException(
            status_code=409,
            detail="Username is already taken",
        ) from error

    return UserCreated(
        id=created_user.id,
        username=created_user.username,
        temporary_password=temporary_password,
    )


@grantavik.post('/auth/login')
def login(user: UserLogin) -> TokenRead:
    checked_user = check_user(user)
    if checked_user is None:
        raise HTTPException(status_code=401, detail="invalid username or password")
    return TokenRead(access_token=create_access_token(checked_user.id))