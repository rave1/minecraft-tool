from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
import settings
import jwt


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
    username: str = Field(unique=True, nullable=False)
    password: str  # hashed
    email: EmailStr | None

    def generate_token(self) -> dict:
        """
        Generate token for user.
        """
        return {
            "access_token": jwt.encode(
                {"username": self.username, "password": self.password},
                key=settings.SECRET_KEY,
            )
        }
