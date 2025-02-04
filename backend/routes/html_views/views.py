from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/login/", response_class=HTMLResponse, tags=["login"], name="login")
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse(
        "login.html",
        context={"request": request, "error": error, "registration_enabled": False},
    )
