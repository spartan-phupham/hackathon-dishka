from uplink import get, response_handler, returns

from service_platform.api.controller.health.schema import HealthResponse
from service_platform.client.base_client import (
    BaseClient,
    logging_error_response,
    raise_for_status,
)


@response_handler(raise_for_status)  # Raise service_platform exception
@response_handler(logging_error_response)  # Logging error when request to client
class HealthClient(BaseClient):
    base_url = "http://0.0.0.0:8080"

    @returns.json(HealthResponse)
    @get("/api/health")
    def check(self):
        pass
