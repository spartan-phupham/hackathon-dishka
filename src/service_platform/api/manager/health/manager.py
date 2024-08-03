from service_platform.api.controller.schema import MessageResponse


class HealthManager:
    def __init__(self) -> None:
        pass

    async def get_heath(self) -> str:
        return "Success"