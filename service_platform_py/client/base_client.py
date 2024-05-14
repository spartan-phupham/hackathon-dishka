from uplink import AiohttpClient, Consumer

from service_platform_py.core.errors import ServiceClientException


def raise_for_status(response):
    if 200 <= response.status_code < 300:
        # Pass through the response.
        return response

    raise ServiceClientException(
        code=response.status,
        message="Can't not access service: {}".format(response.url),
    )


# Response handler, should return response if it don't raise exception
def logging_error_response(response):
    if 200 <= response.status_code < 300:
        # Pass through the response.
        return response
    else:
        print(f"Can't access service: {response.url}. Detail: {response.json()}")
    return response


class BaseClient(Consumer):
    base_url = "http://127.0.0.1:8000"

    def __init__(self, **kwargs):
        super().__init__(client=AiohttpClient(), base_url=self.base_url, **kwargs)
