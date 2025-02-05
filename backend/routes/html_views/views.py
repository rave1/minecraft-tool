from fastapi import Request, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from forms.auth import LoginForm, RegisterForm
from db.auth.tools import get_password_hash, verify_password
from db.auth.models import User
from typing import Annotated
from main import get_session
from sqlmodel import Session, select

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
async def login_user(
    request: Request,
    data: Annotated[LoginForm, Form()],
    session: Annotated[Session, Depends(get_session)],
):
    password = data.password
    try:
        user: User = session.exec(
            select(User).where(User.username == data.username)
        ).one()
        if verify_password(plain_password=password, hashed_password=user.password):
            request.session.update(user.generate_token())
            return RedirectResponse(
                url="/", status_code=302
            )  # https://www.webfx.com/web-development/glossary/http-status-codes/what-is-a-302-status-code/
        else:
            pass
    except Exception as e:
        return templates.TemplateResponse(
            "login.html", context={"request": request, "error": e}
        )


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
            context={"request": request, "error": "Passwords do not match"},
            status_code=400,
        )
    hashed_password = get_password_hash(data.password)
    user = User(username=data.username, password=hashed_password)
    try:
        db.add(user)
        db.commit()
    except Exception as e:
        return templates.TemplateResponse(
            "register.html",
            context={"request": request, "error": "Username taken"},
            status_code=400,
        )
    return {"detail": "Created user."}
