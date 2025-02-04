from typing import Union
from contextlib import asynccontextmanager
from db.engine import init_db, get_session
from typing import Annotated
from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from db.models import User


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/")
def get_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users
