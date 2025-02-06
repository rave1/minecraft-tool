from typing import Union
from contextlib import asynccontextmanager
from db.engine import init_db, get_session
from typing import Annotated
from fastapi import FastAPI, Depends, Request
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from db.auth.tools import AuthHandler
from fastapi import Response
from db.auth.tools import RequiresLoginException
from fastapi.responses import RedirectResponse

# from db.models import User
from routes.html_views.views import router as html_router
from fastapi.staticfiles import StaticFiles
import settings

templates = Jinja2Templates(directory="templates")
auth_handler = AuthHandler()


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


@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    """this handler allows me to route the login exception to the login page."""
    return RedirectResponse(url="/login")


@app.middleware("http")
async def create_auth_header(
    request: Request,
    call_next,
):
    """
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    """
    if "Authorization" not in request.headers and "Authorization" in request.cookies:
        access_token = request.cookies["Authorization"]

        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer {access_token}".encode(),
            )
        )

    response = await call_next(request)
    return response


@app.get("/", name="index")
async def read_root(request: Request, user=Depends(auth_handler.auth_wrapper)):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Home",
            "active_page": "home",
            "user": user,  # Replace with actual user data from your auth system
        },
    )


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
