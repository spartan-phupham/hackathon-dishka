from fastapi.routing import APIRouter

from spartan_api_python.api.views import index

router = APIRouter()
router.include_router(index.router)
