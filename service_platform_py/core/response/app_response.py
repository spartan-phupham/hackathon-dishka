from typing import Any, List, Union

from fastapi.responses import ORJSONResponse

from service_platform_py.core.base_schema import CoreModel


class AppResponseModel(CoreModel):
    """
    Model representing the structure of the application response.

    Attributes:
        result: The result of the response, can be a list, a single object or None.
        messages: Optional list of messages associated with the response.
        success: Boolean indicating the success status of the response.
    """

    result: Union[List[CoreModel], CoreModel, None] = None
    messages: Union[List[str], None] = None
    success: bool = True


class AppResponse(ORJSONResponse):
    """
    Custom JSON response class for the application.

    Attributes:
        media_type: The media type of the response.
    """

    media_type = "application/json"

    def __init__(
        self,
        content: Union[AppResponseModel, Any] = None,
        status_code: int = 200,
        success: bool = True,
    ) -> None:
        """
        Initialize the AppResponse object.

        :param content: The content of the response.
        :param status_code: The HTTP status code of the response.
        :param success: Boolean indicating the success status of the response.
        """
        if isinstance(content, AppResponseModel):
            super().__init__(content.model_dump(exclude_none=True), status_code)
        else:
            content_resp = AppResponseModel()
            content_resp.success = success
            if success is False:
                if isinstance(content, str):
                    content_resp.messages = [content]
                else:
                    content_resp.messages = content
            else:
                content_resp.result = content
                content_resp.messages = ["Successfully"]
            super().__init__(content_resp.model_dump(by_alias=True), status_code)
