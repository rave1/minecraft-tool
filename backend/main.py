from typing import Union
from contextlib import asynccontextmanager
from db.engine import init_db, get_session
from typing import Annotated
from fastapi import FastAPI, Depends, Request
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware

# from db.models import User
from routes.html_views.views import router as html_router
from fastapi.staticfiles import StaticFiles
import settings


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)
app.include_router(html_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.get("/")
def read_root(request: Request):
    return request.session


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# @app.post("/users/")
# def create_user(user: User, session: SessionDep) -> User:
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user


# @app.get("/users/")
# def get_users(
#     session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
# ) -> list[User]:
#     users = session.exec(select(User).offset(offset).limit(limit)).all()
#     return users
