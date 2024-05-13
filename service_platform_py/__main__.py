import uvicorn

from service_platform_py.settings import settings


def main() -> None:
    uvicorn.run(
        "service_platform_py.api.application:get_app",
        workers=settings.workers_count,
        host=settings.address,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level,
        factory=True,
    )


if __name__ == "__main__":
    main()
