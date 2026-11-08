from pydantic import BaseModel, Field, ConfigDict, StringConstraints
from typing import Annotated



class UserLogin(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(min_length=3)
    password: Annotated[
        str,
        StringConstraints(strip_whitespace=False),
    ] = Field(min_length=3)


class UserCreated(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: int
    username: str = Field(min_length=3)
    temporary_password: Annotated[
        str,
        StringConstraints(strip_whitespace=False),
    ] = Field(min_length=3)
    


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(min_length=3)
    role_name: str



class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangeTemporaryPasswordRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=3)

    temporary_password: Annotated[
        str,
        StringConstraints(strip_whitespace=False),
    ] = Field(min_length=3)

    new_password: Annotated[
        str,
        StringConstraints(strip_whitespace=False),
    ] = Field(min_length=3)