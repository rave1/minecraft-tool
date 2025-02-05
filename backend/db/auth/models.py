from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    username: str
    email: EmailStr


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str  # hashed
    email: EmailStr | None
