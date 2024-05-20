from datetime import datetime

import pytz

from service_platform_py.settings import settings


def get_now() -> datetime:
    """
    Retrieves `now` function from the path, specified in project's conf.
    :return: datetime of "now"
    """
    return datetime.now(tz=get_timezone())


def get_timezone():
    """
    Retrieves timezone name from settings and tries to create tzinfo from it.
    :return: tzinfo object
    """
    return pytz.timezone(settings.timezone)
