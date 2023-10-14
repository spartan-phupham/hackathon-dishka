from fastapi import APIRouter

from spartan_api_python.api.router.echo.schema import EchoRequest, EchoResponse


class EchoRouter:
    def __init__(self, router: APIRouter):
        self.router = router
        self.router.add_api_route("/send", self.send, methods=["POST"])

    async def send(self, request: EchoRequest) -> EchoResponse:
        return EchoResponse(message=request.message)
