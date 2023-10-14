from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

router = APIRouter()
templates = Jinja2Templates(directory="spartan_api_python/templates")


@router.get("/")
async def get_index(request: Request) -> Response:
    """
    Return Index html page.

    :param request: Request from client
    :return: Response index.html
    """
    return templates.TemplateResponse("index.html", {"request": request})
