import inspect
import logging


def get_logger():
    # Get the caller's module
    frame = inspect.currentframe().f_back
    module = inspect.getmodule(frame)

    # Extract the part of the module path after 'service_platform'
    module_parts = module.__name__.split(".")
    service_platform_index = module_parts.index("service_platform")
    name = ".".join(module_parts[service_platform_index + 1 :])

    return logging.getLogger(f"service_platform.{name}")
