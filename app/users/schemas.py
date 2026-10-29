from pydantic import BaseModel, Field, ConfigDict, StringConstraints
from typing import Annotated



class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(min_length=3)
    password: Annotated[
        str,
        StringConstraints(strip_whitespace=False),

    ] = Field(min_length=3)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str