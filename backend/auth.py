from fastapi.security import OAuth2PasswordBearer

from typing import Annotated
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi import status, Request
from settings import SECRET_KEY
from db.auth.models import TokenData, User
from jwt.exceptions import InvalidTokenError
from db.auth.tools import get_user
from sqlmodel import Session
from main import get_session
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)],
    request: Request,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(request.session["access_token"], SECRET_KEY)
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db_session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
