import nest_asyncio
import uvicorn

from service_platform.settings import settings
from service_platform.utils.logger import config_logging

nest_asyncio.apply()


def main() -> None:
    log_config = config_logging()
    uvicorn.run(
        f"service_platform.api.application:get_updated_app",
        workers=settings.server.workers_count,
        host=settings.server.address,
        port=settings.server.port,
        reload=settings.server.reload,
        log_level=settings.server.uvicorn_log_level,
        log_config=log_config,
        proxy_headers=settings.server.proxy_headers,
        forwarded_allow_ips=settings.server.forwarded_allow_ips,
        loop="asyncio",
        factory=True,
    )


if __name__ == "__main__":
    main()
