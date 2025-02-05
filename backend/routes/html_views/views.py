from fastapi import Request, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from forms.auth import LoginForm, RegisterForm
from db.auth.tools import get_password_hash, auth_user
from db.auth.models import User
from typing import Annotated
from main import get_session
from sqlmodel import Session

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/login/", response_class=HTMLResponse, tags=["auth"], name="login")
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse(
        "login.html",
        context={"request": request, "error": error, "registration_enabled": True},
    )


@router.get(
    "/register/", response_class=HTMLResponse, tags={"register"}, name="register"
)
async def register_page(request: Request, error: str = None):
    return templates.TemplateResponse(
        "register.html", context={"request": request, "error": error}
    )


@router.post(path="/login/", tags=["auth"])
async def login_user(request: Request, data: Annotated[LoginForm, Form()]):
    username = data.username
    password = data.password
    hashed_password = get_password_hash(password)
    if auth_user(hashed_password):
        pass


@router.post(path="/register/", tags=["auth"])
async def register_user(
    data: Annotated[RegisterForm, Form()],
    request: Request,
    session: Annotated[Session, Depends(get_session)],
):
    db = session
    if data.password != data.password1:
        return templates.TemplateResponse(
            "register.html",
            context={"request": request, "error": "Passwords do not match."},
            status_code=400,
        )
    hashed_password = get_password_hash(data.password)
    user = User(username=data.username, password=hashed_password)
    db.add(user)
    db.commit()
    return {"detail": "Created user."}
