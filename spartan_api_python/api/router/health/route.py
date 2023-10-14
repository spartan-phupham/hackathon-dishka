from fastapi import APIRouter

from spartan_api_python.api.router.health.schema import HealthResponse


class HealthRouter:
    def __init__(self, router: APIRouter):
        super().__init__()
        self.router = router
        self.router.add_api_route("/", self.health, methods=["GET"])

    async def health(self) -> HealthResponse:
        return HealthResponse(message="OK")
